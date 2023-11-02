from django.urls import path
from . import views

urlpatterns = [
    path('project/get/', views.ListAllProjects.as_view(), name='list-projects'),
    path('project/create/', views.CreateProjectAPI.as_view(), name='create-project'),
    path('projects/<int:project_id>/', views.GetProjectByID.as_view(), name='get-project-by-id'),
    path('projects/<int:project_id>/update/', views.UpdateProject.as_view(), name='update-project'),
    path('projects/<int:project_id>/delete/', views.DeleteProject.as_view(), name='delete-project'),
	path('register/', views.RegisterAPI.as_view()),
    path('verify/', views.VerifyOTP.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('user_manage/<int:user_id>/', views.InforUser.as_view()),
    path('me/', views.Me.as_view()),
]
