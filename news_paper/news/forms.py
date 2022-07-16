from django import forms
from django.contrib.auth.models import Group, User
from allauth.account.forms import SignupForm
from .models import Post, Comment


class BasicSignupForm(SignupForm): # Регистрация нового пользователя средствами allauth
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')


class PostForm(forms.ModelForm): # Форма редактирования новости
    class Meta:
        model = Post
        fields = ['title', 'category', 'text']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class PostComment(forms.ModelForm): # Форма редактирования комментария
    class Meta:
        model = Comment
        fields = ['text']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
