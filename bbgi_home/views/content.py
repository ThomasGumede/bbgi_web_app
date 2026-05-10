# consent/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bbgi_home.models import CookieConsent
from bbgi_home.utilities.decorators import get_client_ip

@csrf_exempt
def save_consent(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'})

    try:
        data = json.loads(request.body)

        consent_type = data.get('type')  # accepted | declined | custom
        analytics = data.get('analytics', False)
        page = data.get('page', '')

        # ensure session exists
        if not request.session.session_key:
            request.session.create()

        CookieConsent.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key,
            consent_type=consent_type,
            analytics=analytics,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            page=page
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})