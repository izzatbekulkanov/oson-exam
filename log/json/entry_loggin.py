from django.http import JsonResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from log.models import LogEntry
import json


@csrf_exempt
@login_required
def entry_logging(request):
    if request.method == 'GET':
        logs = LogEntry.objects.all().values(
            'timestamp', 'level', 'message', 'user_full_name', 'browser_name',
            'mac_address', 'device_name', 'global_ip'
        )

        # Convert timestamp to desired format
        formatted_logs = []
        for log in logs:
            log['timestamp'] = log['timestamp'].strftime('%Y-%m-%d | %H:%M:%S')  # Customize this format as needed
            formatted_logs.append(log)

        return JsonResponse(formatted_logs, safe=False)
    else:
        return HttpResponseBadRequest('Invalid request method')
