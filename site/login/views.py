from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.urls import reverse

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            next_url = request.POST.get('next', '') or reverse('auditoriums:auditoriums_list')
            return redirect(next_url)
        
        messages.error(request, "Неверный логин или пароль")
        return render(request, "login/login.html", {
            'error_message': "Неверный логин или пароль",
            'next': request.POST.get('next', '')
        })
    
    return render(request, "login/login.html", {
        'next': request.GET.get('next', '')
    })

def logout(request):
    auth_logout(request)
    return redirect("login:login")