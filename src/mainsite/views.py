from django.shortcuts import render
from django.views.generic.detail import DetailView
# Create your views here.

# register / login / logout stuff
class UserRegisterView:
	pass


class UserLoginView:
	pass


class UserLogoutView:
	pass


# User Self-management stuff
class UserSettingsView:
	pass


class UserPageView(DetailView):
	pass



class ProjectCreateView:
	pass


class ProjectInvitePeopleView:
	pass


class ProjectVacancyListView:
	pass


class ProjectVacancyView:
	pass



# Searching things
class UsersListView:
	pass


class ProjectsListView:
	pass


class VacanciesListView:
	pass