from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now
import json
from attendance.models import AttendanceRecord
from data.auditoriums_urls import AUDITORIUM_URLS


@csrf_exempt
def save_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data['session_id']
            video_url = data['auditorium_id']  # ⚠️ сюда приходит URL, не имя!
            people_count = data['people_count']

            # Найдём имя аудитории по URL
            auditorium_name = next((name for name, url in AUDITORIUM_URLS.items() if url == video_url), None)

            if not auditorium_name:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Не найдена аудитория по URL: {video_url}'
                }, status=400)

            AttendanceRecord.objects.create(
                session_id=session_id,
                auditorium_id=auditorium_name,  # сохраняем 'Т109', например
                people_count=people_count,
                counted_at=now()
            )

            return JsonResponse({'status': 'success'}, status=201)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)