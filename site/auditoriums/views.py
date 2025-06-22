import os
import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from data.auditoriums_urls import AUDITORIUM_URLS

from auditoriums.models import Auditorium
from attendance.models import AttendanceRecord


def auditoriums_list(request):
    if not request.user.is_authenticated:
        return redirect("login:login")

    username = request.user.username

    json_file_path = os.path.join(settings.BASE_DIR, 'data', 'auditoriums_data.json')

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

    json_file_path = os.path.join(settings.BASE_DIR, 'data', 'auditoriums_data.json')

    with open(json_file_path, 'r', encoding='utf-8') as file:
        all_data = json.load(file)
        auditoriums_data = all_data.get(username, [])
        auditorium = next((item for item in auditoriums_data if item['auditorium'] == auditorium_name), None)

    video_url = AUDITORIUM_URLS.get(auditorium['auditorium'])

    request_json = {
        'auditorium_id': auditorium['auditorium'],
        'video_url': video_url,
    }

    res = requests.post('http://localhost:8001/api/start', json=request_json)
    session_id = res.json()['session_id']

    return render(request,
                  'auditoriums/auditorium_detail.html',
                  {'auditorium': auditorium, 'session_id': session_id})


def auditorium_charts(request):
    if not request.user.is_authenticated:
        return redirect("login:login")
    
    auditoriums = Auditorium.objects.all()
    return render(request, 'auditoriums/charts.html', {'auditoriums': auditoriums})


@csrf_exempt
def auditorium_chart_data(request, auditorium_id):
    try:
        # Получаем аудиторию по ID
        auditorium = Auditorium.objects.get(id=auditorium_id)
        
        # Получаем URL видео для этой аудитории
        video_url = AUDITORIUM_URLS.get(auditorium.name)
        
        if not video_url:
            return JsonResponse({'error': f'URL не найден для аудитории {auditorium.name}'}, status=404)

        # Теперь фильтруем по URL видео, который хранится в auditorium_id
        records = AttendanceRecord.objects.filter(
            auditorium_id=video_url
        ).order_by('counted_at')

        print(f"📊 Загружаем данные для аудитории {auditorium.name}")
        print(f"🎥 URL видео: {video_url}")
        print(f"📝 Найдено записей: {records.count()}")

        chart_data = {
            'labels': [r.counted_at.strftime('%Y-%m-%d %H:%M:%S') for r in records],
            'values': [r.people_count for r in records]
        }

        return JsonResponse(chart_data)

    except Auditorium.DoesNotExist:
        return JsonResponse({'error': 'Аудитория не найдена'}, status=404)