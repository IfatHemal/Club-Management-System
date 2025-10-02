from django.contrib import admin   # <-- this was missing
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', lambda request: redirect('login')),  # redirect / to login
]
