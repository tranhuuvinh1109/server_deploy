from django.urls import path
from . import views

urlpatterns = [
    path('train/', views.CreateProjectAPI.as_view(), name='train'),
	# path('register/', views.RegisterAPI.as_view()),
    path('verify/', views.VerifyOTP.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('user_manage/<int:user_id>/', views.InforUser.as_view()),
    path('me/', views.Me.as_view()),
]
