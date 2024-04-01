from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('user-profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('Update-room/<str:pk>/', views.Updateroom, name="Update-room"),
    path('Delete-room/<str:pk>/', views.deleteRoom, name="Delete-room"),
    path('login/', views.LoginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.LogoutPage, name='logout'),
    path('Delete-message/<str:pk>/', views.deleteMessage, name="Delete-message"),
    path('update_user/', views.UpdateUser, name="update_user"),
    path('topics/', views.topicsPage, name="topics"),
     path('activity/', views.activityPage, name="activity"),

]
