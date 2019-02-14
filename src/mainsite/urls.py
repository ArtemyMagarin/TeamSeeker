from django.urls import include, path

from .views import UserRegisterView, UserLoginView, UserLogoutView, UserPageView


urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='registration-view'),
    path('signin/', UserLoginView.as_view(), name='login-view'),
    path('logout/', UserLogoutView.as_view(), name='logout-view'),
    path('user/<int:pk>/', UserPageView.as_view(), name='account-view'),


]