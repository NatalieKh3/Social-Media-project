from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import authenticate, login, logout

def main_page(request):
    return render (request,"users/main.html")

def register_page(request):
    user_form=None
    profile_form=None
    if request.method=="POST":
        user_form=UserCreationForm(request.POST)
        profile_form=ProfileCreationForm(request.POST,request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            my_user=user_form.save()
            profile=profile_form.save(commit=False)
            profile.user=my_user
            profile.save()
            return HttpResponse("user_is_created")
    user_form=UserCreationForm()
    profile_form=ProfileCreationForm()

    context={
        "user_form":user_form,
        "profile_form":profile_form,
    }
    return render(request,"users/register.html",context=context)

def user_logout(request):
    logout(request)
    return redirect("main_page")

def login_page(request):
    error=""
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if len(username)==0 and len(password)==0:
            error="Fill in all lines"
        elif len(username)==0:
            error="Fill in username"
        elif len(password)==0:
            error="Fill in password"
        else:
            user=authenticate(request, username=username, password=password)
            print(user)
            if user is None:
                error="There is no users with such username"
            else:
                login(request,user)
                return redirect("main_page")
    d={
        "error":error
    }
    return render (request,"users/login.html")

def profile_page(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    d={
        "profile":profile
    }
    return render(request, "users/profile.html",context=d)

def friend_list(request):
    Users=User.objects.all()
    profiles=Profile.objects.all()
    possible_friend_request=FriendRequest.objects.all().filter(friend1=request.user, friend_accept=False)
    needed_users=[]
    for i in Users:
        k=0
        for j in possible_friend_request:
            if i==j.friend2:
                k=1
        if k!=1:
            needed_users.append(i)
    needed_profiles=[]
    for i in needed_users:
        print(i.username)
        if i.username!="admin":
            current_profile=Profile.objects.get(user=i)
            needed_profiles.append(current_profile)
    d={
        "profiles":needed_profiles
    }
    # print("users:",needed_users)
    print("profiles",needed_profiles)
    # print(possible_friend_request)
    return render(request, "users/possible_friends.html",context=d)

def add_friend(request,user_id):
    user1=request.user
    user2=User.objects.get(pk=user_id)
    friend_accept=FriendRequest(friend1=user1, friend2=user2, friend_accept=False)
    friend_accept.save()
    return redirect("possible_friends")

def requests(request):
    friend_request=FriendRequest.objects.all().filter(friend2=request.user, friend_accept=False)
    profiles=[]
    for i in friend_request:
        profile=Profile.objects.get(user=i.friend1)
        profiles.append(profile)
    d={
        "profiles":profiles,
    }
    return render(request, "users/requests.html",context=d)

def accept_friend(request,user_id):
    user=User.objects.get(pk=user_id)
    friend_accept=FriendRequest.objects.get(friend1=user,friend2=request.user, friend_accept=False)
    friend_accept.friend_accept=True
    friend_accept.save()
    return redirect("profile_page")
