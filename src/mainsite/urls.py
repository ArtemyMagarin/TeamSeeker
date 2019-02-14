from django.urls import include, path

from .views import (
    UserRegisterView, UserLoginView, UserLogoutView, 
    UserPageView, ProjectCreateView, ProjectListView,
    ProjectDetailView, ProjectUpdateView,
    VacancyCreateView, VacancyListView,  VacancyDetailView,
    VacancyUpdateView,
)


urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='registration-view'),
    path('signin/', UserLoginView.as_view(), name='login-view'),
    path('logout/', UserLogoutView.as_view(), name='logout-view'),

    path('users/<int:pk>/', UserPageView.as_view(), name='account-view'),
    path('users/me/', UserPageView.as_view(), name='my-account-view'),

    path('projects/', ProjectListView.as_view(), name='project-list-view'),
    path('projects/new/',  ProjectCreateView.as_view(), name='project-create-view'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail-view'),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update-view'),
    
    path('projects/<int:project_id>/jobs/', VacancyListView.as_view(), name='vacancy-list-view'),
    path('projects/<int:project_id>/jobs/new/', VacancyCreateView.as_view(), name='vacancy-create-view'),
    path('projects/<int:project_id>/jobs/<int:pk>/', VacancyDetailView.as_view(), name='vacancy-detail-view'),
    path('projects/<int:project_id>/jobs/<int:pk>/update/', VacancyUpdateView.as_view(), name='vacancy-update-view'),
   
    #    Подача заявки
    #    Приглашение в проект
    #    Отображеие заявки в зависимости от того, кто юзер

    #    ---
    #    Скрывать инфу на страницах
    #    Скрывать инфу на проектах
    #    
    # path('projects/<int:project_id>/jobs/<int:pk>/request/', VacancyRequestView.as_view(), name='vacancy-request-view'),
    
    # path('/users/<int:pk>/invite/', ),
    # path('/projects/<int:project_id>/jobs/<int:pk>/request/', ),

]
