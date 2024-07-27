from django.urls import path

from api import views

urlpatterns = [
    path('user/register/', views.UserRegisterAPI.as_view()),  # user register api
    path('user/login/', views.UserLoginAPI.as_view()),  # user login api
    path('event/', views.EventAPI.as_view()),   # event crud api
    path('event/<str:id>/', views.EventAPI.as_view()),  # get single event using id
    path('register/event/', views.EventRegisterAPI.as_view()),  # register event api
    path('report/', views.ReportAPI.as_view()),  # event report api
    path('event-count/', views.CountEventsAPI.as_view()),   # event and user count api
]
