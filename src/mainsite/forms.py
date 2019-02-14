from django import forms
from django.forms import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

from .models import User, Project, AbstractImage, Vacancy 

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=255, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=255, required=True) 
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', required=True, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            self.add_error('password', ValidationError('Введенные пароли не совпадают'))

        try:
            u = User.objects.get(email=email)
            self.add_error('email', ValidationError('Вы не можете использовать этот email'))
        except ObjectDoesNotExist:
            pass

        return cleaned_data


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 
            'description', 
            'status', 
            'estimated_start_date', 
            'estimated_finish_date', 
            'is_published'
        ]


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'project',
            'name', 
            'description', 
            'vacancy_type', 
            'salary', 
            'is_archived'
        ]
    

class UserForm(forms.Form):
    image = forms.ImageField(label='Загрузите аватар', required=False)
    old_password = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput())
    new_password = forms.CharField(label='Новый пароль', required=False, widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Повторите пароль', required=False, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        image = cleaned_data.get('image')
        old_password = cleaned_data.get('old_password')
        password = cleaned_data.get('new_password')
        password2 = cleaned_data.get('new_password2')

        if image != None:
            if image.height <= 500 and image.width <= 200:
                im = AbstractImage()
                im.image = image
                im.save()
                cleaned_data['image'] = im.image.url()
            else:
                self.add_error('image', ValidationError('Максимальный размер аватара 200 x 500 px'))

        if password != password2:
            self.add_error('new_password', ValidationError('Введенные пароли не совпадают'))

       
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        u = authenticate(
            email=email,
            password=password,
        )

        if u is None:
            self.add_error('email', ValidationError('Неверный email или пароль'))            

        return cleaned_data
