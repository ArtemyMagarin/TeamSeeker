from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    LOGIN_METHODS = (
        ('g', 'Login with Google'),
        ('e', 'Login with Email'),
        ('vk', 'Login with VK')
    )

    email = models.EmailField('email', unique=True)
    first_name = models.CharField('name', max_length=255)
    last_name = models.CharField('surname', max_length=255)
    avatar_url = models.URLField(null=True, blank=False)
    login_method = models.CharField(max_length=2, choices=LOGIN_METHODS)
    
    date_joined = models.DateTimeField('registered', auto_now_add=True)
    is_active = models.BooleanField('is_active', default=True)
    is_staff = models.BooleanField('is_staff', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


    def __str__(self):
        return self.get_full_name()


    def get_full_name(self):
        return "{first_name} {last_name}".format(
            first_name=self.first_name, 
            last_name=self.last_name).strip()


    def get_short_name(self):
        return self.first_name.strip()



class VacancyType(models.Model):
    type_name = models.CharField(max_length=255)


class Vacancy(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(null=True, max_length=3000)
    salary = models.CharField(max_length=255, default='По договоренности')
    is_archived = models.BooleanField(default=False)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    vacancy_type = models.ForeignKey(VacancyType, on_delete=models.CASCADE)


class ProjectMember(models.Model):
    MEMBER_STATUSES__IN = 'in'
    MEMBER_STATUSES__INVITED = 'invited'
    MEMBER_STATUSES__ENTRY_REQUEST = 'entry_request'
    MEMBER_STATUSES__INVITE_REJECTED = 'invite_rejected'
    MEMBER_STATUSES__ENTRY_REQUEST_REJECTED = 'entry_request_rejected'
    MEMBER_STATUSES__SELF_LEAVED = 'self_leaved'
    MEMBER_STATUSES__DISMISSED = 'dismissed'

    MEMBER_STATUSES = (
        (MEMBER_STATUSES__IN, 'Участник проекта'),
        (MEMBER_STATUSES__INVITED, 'Приглашен в проект'),
        (MEMBER_STATUSES__ENTRY_REQUEST, 'Отправлен запрос на вступление в команду'),
        (MEMBER_STATUSES__INVITE_REJECTED, 'Приглашение отклонено'),
        (MEMBER_STATUSES__ENTRY_REQUEST_REJECTED , 'Запрос на вступление отклонен'),
        (MEMBER_STATUSES__SELF_LEAVED, 'Уход из проекта по собственной инициативе'),
        (MEMBER_STATUSES__DISMISSED, 'Уход из проекта по инициативе менеджера проекта')
    )

    ROLES__OWNER = 'owner'
    ROLES__MANAGER = 'manager'
    ROLES__EMPLOYEE = 'employee'

    ROLES = (
        (ROLES__OWNER, 'Создатель проекта'),
        (ROLES__MANAGER, 'Менеджер'),
        (ROLES__EMPLOYEE, 'Участник'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=MEMBER_STATUSES)
    role = models.CharField(max_length=20, choices=ROLES)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)


class Project(models.Model):
    PROJECT_STATUSES__RECRUITING = 'recruiting'
    PROJECT_STATUSES__IN_PROGRESS = 'in_progress'
    PROJECT_STATUSES__FINISHED = 'finished'
    PROJECT_STATUSES__PAUSED = 'paused'
    PROJECT_STATUSES__ON_HOLD = 'on_hold'

    PROJECT_STATUSES = (
        (PROJECT_STATUSES__RECRUITING, 'Набор участников'),
        (PROJECT_STATUSES__IN_PROGRESS, 'В процессе'),
        (PROJECT_STATUSES__FINISHED, 'Окончен'),
        (PROJECT_STATUSES__PAUSED, 'Приостановлен'),
        (PROJECT_STATUSES__ON_HOLD, 'Заморожен'),
    )
    

    name = models.CharField(max_length=512)
    description = models.CharField(null=True, max_length=3000)
    status = models.CharField(max_length=20, choices=PROJECT_STATUSES)
    estimated_start_date = models.DateTimeField()
    estimated_finish_date = models.DateTimeField()

    def duration_in_month(self):
        return (((estimated_finish_date - estimated_start_date).days / 30) ** 2) ** 0.5


class WallPost(models.Model):
    message = CharField(max_length=5000)
    # если не указан, значит пост создан автоматически
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # если не указан, значит пост личный, на странице создателя
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

