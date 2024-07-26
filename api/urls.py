from django.urls import path

from api import views

urlpatterns = [
    path('user/register/', views.UserRegisterAPI.as_view()),
    path('user/login/', views.UserLoginAPI.as_view()),
    path('event/', views.EventAPI.as_view()),
    path('event/<str:id>/', views.EventAPI.as_view())
]