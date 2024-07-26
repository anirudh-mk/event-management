from django.urls import path

from api import views

urlpatterns = [
    path('user/register/', views.UserRegisterAPI.as_view()),
    path('user/login/', views.UserLoginAPI.as_view()),
    path('user/a/', views.a.as_view())
]