from django import forms
from .models import MyUser 
from django.contrib.auth import authenticate
from material import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 25)
    password = forms.CharField(widget = forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.authenticated_user = None
        super(LoginForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        data_username = self.cleaned_data.get('username', '')
        if not MyUser.objects.filter(username = data_username).exists():
            raise forms.ValidationError('Invalid Username')
        return data_username

    def clean(self):
        data_username = self.cleaned_data.get('username', '')
        data_password = self.cleaned_data.get('password', '')
        user = authenticate(username = data_username, password = data_password)
        if data_username and data_password and not user:
            raise forms.ValidationError('Username/Password do not match')
        if user and user.is_active == False:
            raise forms.ValidationError('Inactive User')
        self.authenticated_user = user
        return self.cleaned_data

class ForgotPassword(forms.Form):
    username = forms.CharField(max_length = 25)

    def clean_username(self):
        data_username = self.cleaned_data.get('username', '')
        if data_username == '' or not MyUser.objects.filter(username = data_username).exists():
            raise forms.ValidationError('Invalid Username')
        return data_username

class SetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        data_new_password = self.cleaned_data.get('new_password')
        data_confirm_password = self.cleaned_data.get('confirm_password')
        if (data_new_password and data_confirm_password 
                and data_new_password != data_confirm_password):
            raise forms.ValidationError("The two passwords field didn't match")
        return data_confirm_password

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    confirm_password = forms.CharField(widget = forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['phone'].required = False
    
    def clean_email(self):
        data_email = self.cleaned_data.get('email', '')
        if not data_email:
            raise forms.ValidationError('This field is required')
        if MyUser.objects.filter(email = data_email).exists():
            raise forms.ValidationError('User with this email already exist')
        return data_email

    def clean_confirm_password(self):
        data_password = self.cleaned_data.get('password')
        data_confirm_password = self.cleaned_data.get('confirm_password')
        if (data_password != data_confirm_password):
            raise forms.ValidationError("The two passwords field didn't match")
        return data_confirm_password

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'phone', 'first_name', 'last_name']
        
        
class ProfileForm(forms.ModelForm):
    old_password = forms.CharField(widget = forms.PasswordInput, required = False)
    new_password = forms.CharField(widget = forms.PasswordInput, required = False)
    layout = Layout(
        Row('username'),
        Row('email'),
        Row(Span6('first_name'), Span6('last_name')),
        Row(Span2('gender'), Span4('dob'), Span6('phone')),
        Row('old_password', 'new_password')
    )
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
#        self.fields['first_name'].required = True

    def clean_gender(self):
        data_gender = self.cleaned_data['gender']
        if data_gender and (data_gender != 'M' and data_gender != 'F'):
            raise forms.ValidationError('You must specify a valid gender')
        return data_gender

    def clean_old_password(self):
        data_old_password = self.cleaned_data['old_password']
        if data_old_password and not self.instance.check_password(data_old_password):
            raise forms.ValidationError('Incorrect Password')
        return data_old_password

    def clean_new_password(self):
        data_old_password = self.cleaned_data['old_password']
        data_new_password = self.cleaned_data['new_password']
        if not data_old_password and data_new_password:
            raise forms.ValidationError('Please specify old password')
        if data_old_password and not data_new_password:
            raise forms.ValidationError('Please specify new password')
        if data_new_password and data_old_password and data_old_password == data_new_password:
            raise forms.ValidationError('New password should not be same as old password')
        return data_new_password
    
    def clean_username(self):
        data_username = self.cleaned_data['username']
        if data_username != self.instance.username:
            raise forms.ValidationError('Invalid Username')
        return data_username
    
    def clean_email(self):
        data_email = self.cleaned_data['email']
        if data_email != self.instance.email:
            raise forms.ValidationError('Invalid Email')
        return data_email
    
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'dob', 'phone']
