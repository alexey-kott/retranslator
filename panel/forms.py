from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField, ModelForm

from panel.models import Account


class SignUpForm(UserCreationForm):
    username = EmailField(max_length=254, help_text='Required. Inform a valid email address.', label='Email')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class NewAccountForm(ModelForm):

    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'phone']