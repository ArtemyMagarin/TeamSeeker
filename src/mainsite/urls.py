from django.urls import include, path

from .views import (
    UserRegisterView, UserLoginView, UserLogoutView, 
    UserPageView, ProjectCreateView, VacancyCreateView
)


urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='registration-view'),
    path('signin/', UserLoginView.as_view(), name='login-view'),
    path('logout/', UserLogoutView.as_view(), name='logout-view'),
    path('users/<int:pk>/', UserPageView.as_view(), name='account-view'),
    path('users/me/', UserPageView.as_view(), name='my-account-view'),
    path('projects/new/',  ProjectCreateView.as_view(), name='project-create-view'),
    path('projects/<int:project_id>/jobs/new/', VacancyCreateView.as_view(), name='vacancy-create-view')

    # path('/users/<int:pk>/invite/', ),
    # path('/projects/<int:project_id>/jobs/<int:pk>/request/', ),
    
]
