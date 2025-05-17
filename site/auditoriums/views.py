import json
import os
from django.shortcuts import render, redirect
from django.conf import settings


def auditoriums_list(request):
    if "username" not in request.session:
        return redirect("login:login")

    username = request.session["username"]

    json_file_path = os.path.join(
        settings.BASE_DIR, 'data', 'auditoriums_data.json')

    with open(json_file_path, 'r', encoding='utf-8') as file:
        all_data = json.load(file)
        auditoriums_data = all_data.get(username, [])

    return render(request,
                  'auditoriums/auditoriums.html',
                  {'auditoriums_data': auditoriums_data})


def auditorium_detail(request, auditorium_name):
    if "username" not in request.session:
        return redirect("login:login")

    username = request.session["username"]

    json_file_path = os.path.join(
        settings.BASE_DIR, 'data', 'auditoriums_data.json')

    with open(json_file_path, 'r', encoding='utf-8') as file:
        all_data = json.load(file)
        auditoriums_data = all_data.get(username, [])
        auditorium = next(
            (item for item in auditoriums_data if item["auditorium"] == auditorium_name), None)

    return render(request,
                  'auditoriums/auditorium_detail.html',
                  {'auditorium': auditorium})
