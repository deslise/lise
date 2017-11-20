from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from managedata.models import EarlyBusinessPlan, RequestCategory


class RegisterForm(UserCreationForm):

    phone = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('first_name', 'email', 'phone', 'password1', 'password2',)


    def clean(self):
        data = self.cleaned_data
        email_all = list(map(lambda u: u.email, User.objects.all()))
        if data.get('email') in email_all:
            raise forms.ValidationError('Este email já está registrado.')
        return data


class NewPlanForm(forms.ModelForm):
    branch = forms.CharField(max_length=240)
    specialty = forms.CharField(max_length=240)

    class Meta:
        model = EarlyBusinessPlan
        fields = ('description', 'state', 'city', 'branch', 'specialty')


    def clean(self):
        data = self.cleaned_data
        return data


class RequestCategoryForm(forms.ModelForm):

    class Meta:
        model = RequestCategory
        fields = ('description', 'branch', 'specialty')


    def clean(self):
        data = self.cleaned_data
        return data


class EditDescriptionPlan(forms.ModelForm):
    id = forms.IntegerField()

    class Meta:
        model = EarlyBusinessPlan
        fields = ('description','id')


    def clean(self):
        data = self.cleaned_data
        return data


class EditMyAccount(forms.ModelForm):
    phone = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('first_name','phone')


    def clean(self):
        data = self.cleaned_data
        return data