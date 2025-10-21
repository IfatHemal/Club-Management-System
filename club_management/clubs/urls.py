from django.urls import path
from .views import  CustomLoginView

app_name = 'clubs'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),

]