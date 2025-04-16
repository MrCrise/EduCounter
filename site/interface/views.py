import json
import os
from django.shortcuts import render, redirect
from django.conf import settings

USERS = [
    {"username": "хозяин", "password": "123"},
    {"username": "новиков", "password": "123"},
]

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        for user in USERS:
            if user["username"] == username and user["password"] == password:
                request.session["username"] = username
                return redirect("auditoriums")
            
        error_message = "Неверный логин или пароль"
        return render(request, "interface/login.html", {"error_message": error_message})
    
    return render(request, "interface/login.html")

def auditoriums(request):
    if "username" not in request.session:
        return redirect("login")
    
    username = request.session["username"]
    
    json_file_path = os.path.join(settings.BASE_DIR, 'data', 'auditoriums_data.json')
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        all_data = json.load(file)
        auditoriums_data = all_data.get(username, [])

    return render(request, 'interface/auditoriums.html', {'auditoriums_data': auditoriums_data})

def auditorium_detail(request, auditorium_name):
    if "username" not in request.session:
        return redirect("login")
    
    username = request.session["username"]
    
    json_file_path = os.path.join(settings.BASE_DIR, 'data', 'auditoriums_data.json')
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        all_data = json.load(file)
        auditoriums_data = all_data.get(username, [])
        auditorium = next((item for item in auditoriums_data if item["auditorium"] == auditorium_name), None)

    return render(request, 'interface/auditorium_detail.html', {'auditorium': auditorium})

def logout(request):
    if "username" in request.session:
        del request.session["username"]
    return redirect("login")