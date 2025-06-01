import cv2
import json
import os
import requests
from django.http import StreamingHttpResponse, Http404
from django.shortcuts import render, redirect
from django.conf import settings
from data.auditoriums_urls import AUDITORIUM_URLS


def auditoriums_list(request):
    if not request.user.is_authenticated:
        return redirect("login:login")

    username = request.user.username

    json_file_path = os.path.join(
        settings.BASE_DIR, 'data', 'auditoriums_data.json')

    with open(json_file_path, 'r', encoding='utf-8') as file:
        all_data = json.load(file)
        auditoriums_data = all_data.get(username, [])

    return render(request,
                  'auditoriums/auditoriums.html',
                  {'auditoriums_data': auditoriums_data})


def auditorium_detail(request, auditorium_name):
    if not request.user.is_authenticated:
        return redirect("login:login")

    username = request.user.username

    json_file_path = os.path.join(
        settings.BASE_DIR, 'data', 'auditoriums_data.json')

    with open(json_file_path, 'r', encoding='utf-8') as file:
        all_data = json.load(file)
        auditoriums_data = all_data.get(username, [])
        auditorium = next(
            (item for item in auditoriums_data if item['auditorium'] == auditorium_name), None)

    video_url = AUDITORIUM_URLS[auditorium['auditorium']]

    request_json = {
        'auditorium_id': auditorium['auditorium'],
        'video_url': video_url,
    }

    res = requests.post('http://localhost:8001/api/start', json=request_json)
    session_id = res.json()['session_id']

    return render(request,
                  'auditoriums/auditorium_detail.html',
                  {
                      'auditorium': auditorium,
                      'session_id': session_id,
                  })
