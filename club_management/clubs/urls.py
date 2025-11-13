from django.urls import path
from . import views
from .views import  CustomLoginView, SignUpView, logout_view

app_name = 'clubs'

urlpatterns = [
path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('head/dashboard/', views.head_dashboard, name='head_dashboard'),
    path('user/add/', views.add_user, name='add_user'),
    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('club/dashboard/', views.club_dashboard, name='club_dashboard'),
    path('club/<slug:slug>/', views.club_detail, name='club_detail'),
    path('club/<slug:club_slug>/add-member/', views.add_member, name='add_member'),
    path('create-club/', views.create_club, name='create_club'),
    path('modify-club/<slug:slug>/', views.modify_club, name='modify_club'),
    path('delete-club/<slug:slug>/', views.delete_club, name='delete_club'),
    path('club/<slug:slug>/members/', views.manage_members, name='manage_members'),
    path('modify-member/<int:pk>/', views.modify_member, name='modify_member'),
    path('delete-member/<int:pk>/', views.delete_member, name='delete_member'),
]

