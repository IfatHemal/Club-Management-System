from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import SignUpForm, ClubForm, MemberForm
from .models import Club, Member, User

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
