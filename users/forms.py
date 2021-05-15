from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account


class RegisterForm(UserCreationForm):
    email           = forms.EmailField(max_length=60, label="Please enter your email adress.")
    username        = forms.CharField(max_length=10, label="Unique Username.")
    description     = forms.CharField(max_length=60,
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Not Required",
                "rows": 4,
                "cols": 50,
            }
        ),
    )


    class Meta:
        model = Account
        fields = (
            'email',
            'username',
            'description',
            'password1',
            'password2',
        )


    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            if '/' in username or '.' in username or ' ' in username:
                raise forms.ValidationError('Username cant contain symbols!')
            return username   


class AuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)


    class Meta:
        model = Account
        fields = (
            'email',
            'password',
        )

    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')


class AccountUpdateForm(forms.ModelForm):


    description = forms.CharField(max_length=60,
            required=False,
            widget=forms.Textarea(
                attrs={
                    "placeholder": "Not Required",
                    "rows": 4,
                    "cols": 50,
                }
            ),
        )


    class Meta:
        model = Account
        fields = (
            'username',
            'description'
        )


    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
                raise forms.ValidationError('Username %s already exists' % username)
            except Account.DoesNotExist:
                if '/' in username or '.' in username or ' ' in username:
                    raise forms.ValidationError('Username cant contain symbols!')
                return username