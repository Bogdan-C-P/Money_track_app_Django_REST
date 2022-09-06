from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Payment
from django.forms import ModelForm

class PaymentForm(ModelForm):
    class Meta:
        model =Payment
        fields = ['title','ammount']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
        