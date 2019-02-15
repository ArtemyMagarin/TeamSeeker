from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic import RedirectView, ListView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.auth import logout, login, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin

from .forms import RegisterForm, LoginForm, ProjectForm, VacancyForm
from .models import User, Project, ProjectMember, Vacancy


class UserLoginView(UserPassesTestMixin, AccessMixin, FormView):
    form_class = LoginForm
    template_name = 'login-form.html'

    def test_func(self):
        return not self.request.user.is_authenticated

    def get_success_url(self):
        return reverse_lazy('account-view', kwargs={'pk': self.request.user.id})

    def handle_no_permission(self):
        return redirect(self.get_success_url())

    def form_valid(self, form):
        u = authenticate(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password'),
        )
        login(self.request, u)
        return super().form_valid(form)


# register / login / logout stuff
class UserRegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register-form.html'
    success_url = reverse_lazy('login-view')

    def form_valid(self, form):
        u = User.objects.create_user(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password'),
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
            login_method='e',
        )
        return super().form_valid(form)


class UserLogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('login-view')

    login_url = reverse_lazy('login-view')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(UserLogoutView, self).get(request, *args, **kwargs)


# User Self-management stuff
class UserSettingsView:
    pass


class UserPageView(DetailView):
    model = User
    template_name = 'user-page.html'

    def dispatch(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
           return redirect(reverse_lazy('account-view', kwargs={'pk': self.request.user.id}))
        return super().dispatch(request, *args, **kwargs)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['me'] = self.request.user
        context['is_my_page'] = self.request.user == context['object']
        return context


class ProjectCreateView(FormView):
    form_class = ProjectForm
    template_name = 'create-project-page.html'

    def form_valid(self, form):
        p = Project.objects.create(**form.cleaned_data)
        pm = ProjectMember.objects.create(
            user=self.request.user,
            status='in',
            role='owner',
            project=p
        )
        return super().form_valid(form)


class ProjectListView(ListView):
    model = Project
    paginate_by = 20
    template_name = 'list-project-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'details-project-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectUpdateView(UpdateView):
    form_class = ProjectForm
    template_name = 'create-project-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Project.objects.filter(
            projectmember__role='owner', 
            projectmember__user=self.request.user,
            pk=self.kwargs['pk'])



class VacancyListView(ListView):
    model = Vacancy
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class VacancyDetailView(DetailView):
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class VacancyUpdateView(UserPassesTestMixin, AccessMixin, UpdateView):
    form_class = VacancyForm
    template_name = 'create-project-page.html'

    def test_func(self):
        p = get_object_or_404(Project, pk=self.kwargs['project_id'])
        r = ProjectMember.objects.filter(
                Q(project=p) &
                Q(status='in') &
                Q(user=self.request.user) &
                (Q(role='owner') | Q(role='manager'))
            ).values()
        return len(r) > 0

    def handle_no_permission(self):
        return redirect(self.get_success_url())

    def get_queryset(self):
        return Vacancy.objects.filter(
            project__projectmember__role='owner', 
            project__projectmember__user=self.request.user,
            project__pk=self.kwargs['project_id'],
            pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('vacancy-detail-view', kwargs={'project_id': self.kwargs['project_id'], 'pk':self.kwargs['pk']})



class VacancyCreateView(UserPassesTestMixin, AccessMixin, FormView):
    form_class = VacancyForm
    template_name = 'create-project-page.html'


    def get_success_url(self):
        return reverse_lazy('vacancy-detail-view', kwargs={'project_id': self.kwargs['project_id'], 'pk': self.kwargs['pk']})


    def test_func(self):
        p = get_object_or_404(Project, pk=self.kwargs['project_id'])
        r = ProjectMember.objects.filter(
                Q(project=p) &
                Q(status='in') &
                Q(user=self.request.user) &
                (Q(role='owner') | Q(role='manager'))
            ).values()
        return len(r) > 0

    def handle_no_permission(self):
        return redirect(reverse_lazy('vacancy-list-view', kwargs={'project_id': self.kwargs['project_id']}))


    def get_initial(self):
        initial = super(VacancyCreateView, self).get_initial()
        p = get_object_or_404(Project, pk=self.kwargs['project_id'])
        initial['project'] = p
        return initial


    def form_valid(self, form):
        v = Vacancy.objects.create(**form.cleaned_data)
        pm = ProjectMember.objects.create(
            user=self.request.user,
            status='in',
            role='owner',
            project=form.cleaned_data['project'],
            vacancy=v
        )
        return super().form_valid(form)


class VacancyRequestView(View):

    def get_success_url(self):
        return reverse_lazy('vacancy-detail-view', kwargs={'project_id': self.kwargs['project_id'], 'pk':self.kwargs['pk']})

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        status = 'entry_request'
        role = 'employee'
        vacancy = get_object_or_404(Vacancy, pk=kwargs.get('pk', 0))
        project = vacancy.project
        pm = ProjectMember.objects.create(
            user=user,
            status=status,
            role=role,
            project=project,
            vacancy=vacancy
        )
        return super().dispatch(self, request, *args, **kwargs)


class VacancyInviteView(UserPassesTestMixin, AccessMixin, View):
    def get_success_url(self):
        return reverse_lazy('account-view', kwargs={'pk':self.kwargs['pk']})

    def test_func(self):
        vacancy = get_object_or_404(Vacancy, pk=kwargs.get('vacancy_id', 0))
        project = vacancy.project
        r = ProjectMember.objects.filter(
                Q(project=project) &
                Q(status='in') &
                Q(user=self.request.user) &
                (Q(role='owner') | Q(role='manager'))
            ).values()

        return len(r) > 0


    def handle_no_permission(self):
        return redirect(reverse_lazy('account-view', kwargs={'pk':self.kwargs['pk']}))



    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('pk', 0))
        status = 'invited'
        role = 'employee'
        vacancy = get_object_or_404(Vacancy, pk=kwargs.get('vacancy_id', 0))
        project = vacancy.project
        pm = ProjectMember.objects.create(
            user=user,
            status=status,
            role=role,
            project=project,
            vacancy=vacancy
        )
        return super().dispatch(self, request, *args, **kwargs)


class ProjectRequestsListView(ListView):
    model = ProjectMember
    paginate_by = 20

    def get_queryselect(self, **kwargs):
        return ProjectMember.objects.filter(
            Q(project__pk=kwargs['project_id']) &
            Q(status='entry_request')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserRequestsListView(ListView):
    model = ProjectMember
    paginate_by = 20

    def get_queryselect(self, **kwargs):
        return ProjectMember.objects.filter(
            Q(user__pk=kwargs['user_id']) &
            Q(status='entry_request')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectInvitesListView(ListView):
    model = ProjectMember
    paginate_by = 20

    def get_queryselect(self, **kwargs):
        return ProjectMember.objects.filter(
            Q(project__pk=kwargs['project_id']) &
            Q(status='invited')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserInvitesListView(ListView):
    model = ProjectMember
    paginate_by = 20

    def get_queryselect(self, **kwargs):
        return ProjectMember.objects.filter(
            Q(user__pk=kwargs['user_id']) &
            Q(status='invited')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class RequestsDetailView(DetailView):
    model = ProjectMember

    def get_queryselect(self, **kwargs):
        if 'user_id' in kwargs:
            return ProjectMember.objects.filter(
                Q(user__pk=kwargs['user_id']) &
                Q(status='entry_request')
            )
        elif 'project_id' in kwargs:
            return ProjectMember.objects.filter(
                Q(project__pk=kwargs['project_id']) &
                Q(status='entry_request')
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['me'] = self.request.user
        return context


class InvitesDetailView(DetailView):
    model = ProjectMember

    def get_queryselect(self, **kwargs):
        if 'user_id' in kwargs:
            return ProjectMember.objects.filter(
                Q(user__pk=kwargs['user_id']) &
                Q(status='invited')
            )
        elif 'project_id' in kwargs:
            return ProjectMember.objects.filter(
                Q(project__pk=kwargs['project_id']) &
                Q(status='invited')
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['me'] = self.request.user
        return context


class RequestInviteActionView(UserPassesTestMixin, AccessMixin, View):

    def test_func(self):
        user = self.request.user
        pm = get_object_or_404(ProjectMember, pk=kwargs.get('pk', 0))

        return (pm.user == user or len(ProjectMember.objects.filter(
                Q(project=pm.project) &
                Q(status='in') &
                Q(user=user) &
                (Q(role='owner') | Q(role='manager'))
            ).values()) > 0) and kwargs.get('action') in ['accept', 'reject', 'delete']

    def get_success_url(self):
        url = reverse_lazy('my-account-view')
        if 'user_id' in kwargs:
            pm = get_object_or_404(ProjectMember, pk=kwargs.get('pk', 0))
            url = reverse_lazy('project-detail-view', kwargs={'pk': pm.project.id})
        elif 'project_id' in kwargs:
            url = reverse_lazy('project-detail-view', kwargs={'pk': kwargs['project_id']})
        
        return url       

    def handle_no_permission(self):
        return redirect(self.get_success_url())
 


    def dispatch(self, request, *args, **kwargs):
        pm = get_object_or_404(ProjectMember, pk=kwargs.get('pk', 0))
        action = kwargs.get('action')

        if action == 'accept':
            pm.status = 'in'
            pm.save()

        if action == 'reject':
            if pm.status == 'invited':
                pm.status = 'invite_rejected'
            if pm.status == 'entry_request':
                pm.status = 'entry_request_rejected'
            pm.save()

        if action == 'delete':
            if pm.status == 'entry_request' and pm.user == request.user:
                pm.delete()

            if pm.status == 'invited' and pm.user != request.user:
                pm.delete()

        return super().dispatch(self, request, *args, **kwargs)




# Searching things
class UsersListView:
    pass


class ProjectsListView:
    pass


class VacanciesListView:
    pass