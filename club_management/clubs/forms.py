from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Club, Member

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('name', 'slug', 'description', 'profile_pic', 'club_admin')

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('full_name', 'profile_pic', 'role', 'email')

class HeadMemberForm(forms.ModelForm):
        club = forms.ModelChoiceField(queryset=Club.objects.all(), required=True, label="Select Club")

        class Meta:
                model = Member
                fields = ['full_name', 'profile_pic', 'email', 'role', 'club']



