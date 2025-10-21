from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm

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
