from django.db.models import Q
from django.shortcuts import render , redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponse
from .models import Room , Topic , Message,User
from .forms import RoomForm , UserCreationForm , updateForm
from django.contrib.auth import authenticate, login, logout



# Create your views here.

# rooms=[
#     {'id':1 , 'name':"acher nizamani"},
#     {'id':2 , 'name':"ayaz nizamani"},
#     {'id':3 , 'name':"awais nizamani"},

# ]

def home(request):
    
    #just for count all
    all_rooms=Room.objects.all()
    rooms=Room.objects.all()
    topics=Topic.objects.all()[0:5]  
    room_msg = Message.objects.all()
    
    if request.method=="GET":
        st=request.GET.get('q')
        if st!=None:
            rooms=Room.objects.filter(
            Q(topic__name__icontains=st))
            topics=Topic.objects.all()[0:5] 
            room_msg = Message.objects.filter(Q(room__topic__name__icontains=st))
        room_filter=rooms.count()    
        topic_count=topics.count()
    
    context={
        'rooms':rooms ,
        'topics':topics,
        'topic_count': topic_count ,
        'room_message' : room_msg,
        'room_filter': room_filter}

    
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_msg = room.message_set.all().order_by('-created')
    participents= room.participents.all()
    participents_count=participents.count()
   
    context = {'room':room, 'room_msg':room_msg , 'participents':participents,'participents_count':participents_count}  
    if request.method=='POST':
        messages=Message.objects.create(
            user=request.user ,
            room=room,
            body=request.POST.get('body')


        )
        room.participents.add(request.user)
        return redirect('room' , pk=room.id)


    return render(request, 'base/room.html',context)
    
def userProfile(request,pk):
    all_rooms= Room.objects.all()
    room_count=all_rooms.count()
    user= User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_msg = user.message_set.all()
    topics=Topic.objects.all() 
    
    context={ 'user':user , 'rooms': rooms , 'room_message':room_msg ,'topics':topics , 'room_count': room_count}
    return render(request,'base/user_profile.html',context)

    
@login_required(login_url='login')
def createRoom(request):
    
    
    form= RoomForm()
    topics=Topic.objects.all()

    
    if request.method=='POST':
        
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)

        x = Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),

        )
        x.participents.add(request.user)
        
        
    
        return redirect('home')
    context={'form':form , 'topics' : topics} 
    return render(request, 'base/room_form.html',context) 
@login_required(login_url='login')
def Updateroom(request,pk):
    x="update"
    room=Room.objects.get(id=pk)
    topics=Topic.objects.all()
    form=RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('sorry your are not allowed')

    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('room' , pk=room.id )

    context={'form':form,'topics' : topics,'room':room , 'page':x}
    return render(request, 'base/room_form.html',context)     
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('sorry your are not allowed')

    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{"obj":room})  



def LoginPage(request):
   
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user=User.objects.get(email=email)
            user=authenticate(request, email=email , password=password ) 
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, "User OR password incorrect")
        except:
            messages.error(request, 'User doesnt exist')    
          
        
    return render(request,'base/login.html')
def LogoutPage(request):
    page='register'
    logout(request)
    return redirect('login')


def registerPage(request):
    form = UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request , user)
            return redirect('home')
        else:
            messages.error(request, 'input valid data OR it can be error occurd during registration')        
    return render(request,'base/signup.html',{'form':form})    

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method=="POST":
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{"obj":message})  

def UpdateUser(request):
    user=request.user
    form=updateForm(instance=user)

    if request.method== "POST" :
        form= updateForm(request.POST , request.FILES ,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context={
        'form': form
    }



    return render(request, 'base/update_user.html', context)

def topicsPage(request):
    topics=Topic.objects.filter()
    topic_count=topics.count()
    if request.method=="GET":
        st=request.GET.get('q')
        if st!=None:
            topics=Topic.objects.filter(
            Q(name__icontains=st))
            topic_count=topics.count()
    
    context={ 
             'topics':topics,
             'topic_count':topic_count}
    return render(request, 'base/topics.html',context)
def activityPage(request):
    room_message = Message.objects.all()
    return render(request,"base/activity.html",{'room_message':room_message})
