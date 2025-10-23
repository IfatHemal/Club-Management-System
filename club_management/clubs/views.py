from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .forms import SignUpForm, ClubForm, MemberForm
from .models import Club, Member, User
from django.db import transaction
from django.contrib import messages

def head_admin_required(user):
    return hasattr(user, 'role') and user.role==User.Role.HEAD_ADMIN

def club_admin_required(user):
    return hasattr(user, 'role') and user.role == User.Role.CLUB_ADMIN

class SignUpView(View):
    template_name = 'clubs/signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('clubs:home')
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    template_name = 'clubs/login.html'

    def get_success_url(self):
        user = self.request.user

        try:
            role = user.role
        except Exception:
            return reverse_lazy('clubs:home')

        if role == User.Role.HEAD_ADMIN:
            return reverse_lazy('clubs:head_dashboard')
        if role == User.Role.CLUB_ADMIN:
            return reverse_lazy('clubs:club_dashboard')
        return reverse_lazy('clubs:home')
@login_required
def logout_view(request):
    logout(request)
    return redirect('clubs:login')
@login_required
def home(request):
    query = request.GET.get('q')
    clubs = Club.objects.all().order_by('name')
    if query:
        clubs = clubs.filter(name__icontains=query)
    return render(request, 'clubs/home.html', {'clubs': clubs, 'query': query})
@login_required
def club_detail(request, slug):
    club = get_object_or_404(Club, slug=slug)
    members = club.members.all()
    return render(request, 'clubs/club_detail.html', {'club': club, 'members': members})
@user_passes_test(head_admin_required)
def head_dashboard(request):
    clubs = Club.objects.all().order_by('name')
    return render(request, 'clubs/head_dashboard.html', {'clubs': clubs})
@user_passes_test(head_admin_required)
def create_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                club = form.save(commit=False)
                club.save()
                new_admin = form.cleaned_data.get('club_admin')
                if new_admin:

                    if new_admin.role != User.Role.CLUB_ADMIN:
                        new_admin.role = User.Role.CLUB_ADMIN
                        new_admin.save()
                messages.success(request, f'Club "{club.name}" created.')
            return redirect('clubs:head_dashboard')
    else:
        form = ClubForm()
    return render(request, 'clubs/create_club.html', {'form': form})
@user_passes_test(club_admin_required)
def modify_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    club = member.club
    if club.club_admin != request.user:
        return HttpResponseForbidden('You cannot edit this member.')
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f'Member "{member.full_name}" updated.')
            return redirect('clubs:manage_members', slug=club.slug)
    else:
        form = MemberForm(instance=member)
    return render(request, 'clubs/modify_member.html', {'form': form, 'member': member})
@user_passes_test(club_admin_required)
def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    club = member.club
    if club.club_admin != request.user:
        return HttpResponseForbidden('You cannot delete this member.')
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Member deleted.')
        return redirect('clubs:manage_members', slug=club.slug)
    return render(request, 'clubs/confirm_delete.html', {'object': member, 'type': 'member'})
@user_passes_test(club_admin_required)
def add_member(request, club_slug):
    club = get_object_or_404(Club, slug=club_slug)

    if club.club_admin != request.user:
        return HttpResponseForbidden('You are not the admin of this club.')

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.club = club
            member.save()
            messages.success(request, f'Member "{member.full_name}" added to {club.name}.')
            return redirect('clubs:manage_members', slug=club.slug)
    else:
        form = MemberForm()
    return render(request, 'clubs/add_member.html', {'form': form, 'club': club})
@user_passes_test(club_admin_required)
def club_dashboard(request):

    clubs = request.user.managed_clubs.all()
    return render(request, 'clubs/club_admin_dashboard.html', {'clubs': clubs})
@user_passes_test(club_admin_required)
def manage_members(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if club.club_admin != request.user:
        return HttpResponseForbidden("You are not the admin of this club.")
    members = club.members.all().order_by('full_name')
    return render(request, 'clubs/manage_members.html', {'club': club, 'members': members})
@user_passes_test(head_admin_required)
def delete_club(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if request.method == 'POST':
        club.delete()
        messages.success(request, f'Club \"{club.name}\" deleted.')
        return redirect('clubs:head_dashboard')

    return render(request, 'clubs/club_delete.html', {'object': club, 'type': 'club'})
@user_passes_test(head_admin_required)
def modify_club(request, slug):
    club = get_object_or_404(Club, slug=slug)
    old_admin = club.club_admin
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            with transaction.atomic():
                club = form.save(commit=False)
                club.save()
                new_admin = form.cleaned_data.get('club_admin')


                if old_admin and old_admin != new_admin:
                    still_admin_elsewhere = old_admin.managed_clubs.exclude(pk=club.pk).exists()
                    if not still_admin_elsewhere:
                        old_admin.role = User.Role.NORMAL
                        old_admin.save()


                if new_admin and new_admin.role != User.Role.CLUB_ADMIN:
                    new_admin.role = User.Role.CLUB_ADMIN
                    new_admin.save()

                messages.success(request, f'Club "{club.name}" updated.')
            return redirect('clubs:head_dashboard')
    else:
        form = ClubForm(instance=club)
    return render(request, 'clubs/modify_club.html', {'form': form, 'club': club})