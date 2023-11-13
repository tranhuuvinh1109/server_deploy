from django.urls import path
from . import views

urlpatterns = [
    path('project/get/', views.ListAllProjects.as_view(), name='list-projects'),
    path('project/create/', views.CreateProjectAPI.as_view(), name='create-project'),
    path('project/<int:project_id>/', views.GetProjectByID.as_view(), name='get-project-by-id'),
    path('project/<int:project_id>/update/', views.UpdateProject.as_view(), name='update-project'),
    path('project/<int:project_id>', views.DeleteProject.as_view(), name='delete-project'),
	path('register/', views.RegisterAPI.as_view()),
    path('verify/', views.VerifyOTP.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('user_manage/', views.InforUser.as_view()),
    path('user_manage/check-worker/', views.CheckWorker.as_view()),
    path('user_manage/all/', views.DashboardProjectAPI.as_view()),
    path('user/', views.GetUserByID.as_view()),
	path('search/', views.SearchAPI.as_view(), name='search'),
	path('realtime/', views.RealtimeAPI.as_view(), name='RealtimeAPI'),
    path('me/', views.Me.as_view()),
]
