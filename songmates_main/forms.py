from django import forms
from django.contrib.auth.models import User


class UserDeleteForm:
    class Meta:
        model = User
        your_name = forms.CharField(label='Your name', max_length=100)