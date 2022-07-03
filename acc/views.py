from email import message
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, "acc/index.html")

def login_user(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        u = authenticate(username=un, password=up)
        if u:
            login(request, u)
            messages.success(request, f"{u} WELCOME !")
            return redirect("acc:index")
        else:
            messages.info(request, "계정정보가 일치하지 않습니다.")
    return render(request, "acc/login.html")

def logout_user(request):
    logout(request)
    return redirect("acc:index")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        uc = request.POST.get("con")
        upic = request.FILES.get("pic")
        try:
            User.objects.create_user(username=un, password=up, content=uc, pic=upic)
            messages.success(request, f"{un} WELCOME !")
            return redirect("acc:login")
        except:
            messages.error(request, "SIGNUP FAIL")
    return render(request, "acc/signup.html")

def profile(request):
    return render(request, "acc/profile.html")

def update(request):
    if request.method == "POST":
        u = request.user
        ue = request.POST.get("umail")
        uc = request.POST.get("ucon")
        up = request.FILES.get("upic")
        u.email, u.content = ue, uc
        if up:
            u.pic.delete()
            u.pic = up
        u.save()
        return redirect("acc:profile")
    return render(request, "acc/update.html")

def changepw(request):
    u = request.user
    cp = request.POST.get("cpass")
    if check_password(cp, u.password):
        np = request.POST.get("npass")
        u.set_password(np)
        u.save()
        messages.success(request, "SUCCESS CHANGE PASSWORD")
        return redirect("acc:login")
    else:
        messages.error(request, "FAIL CHANGE PASSWORD")
    return redirect("acc:update")

def delete(request):
    u = request.user
    cp = request.POST.get("cpass")
    if check_password(cp, u.password):
        if u.pic:
            u.pic.delete()
        u.delete()
        messages.success(request, "SUCCESS DELETE")
        return redirect("acc:index")
    else:
        messages.error(request, "FAIL DELETE")
        return redirect("acc:profile")