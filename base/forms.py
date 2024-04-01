from django.forms import ModelForm
from .models import Room 

from .models import User
from django.contrib.auth.forms import UserCreationForm

# Myuser = get_user_model()






class RoomForm(ModelForm):
    
    class Meta:
        model = Room 
        fields = '__all__'
        exclude = ['host','admin']

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email','bio','password1','password2','avtar']

class updateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','bio','avtar']
           

