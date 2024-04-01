from django.contrib import admin
from .models import Room  , Message , Topic 
from django.contrib.auth import get_user_model
User = get_user_model()



# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(User)