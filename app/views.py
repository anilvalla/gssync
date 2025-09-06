import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from .models import Slate

def home_page(request):
    return render(request, 'home.html')

def basic_auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Get credentials from environment variables
        API_USERNAME = os.environ.get('API_USERNAME')
        API_PASSWORD = os.environ.get('API_PASSWORD')

        # Check for Authorization header
        if 'HTTP_AUTHORIZATION' not in request.META:
            response = HttpResponse('Unauthorized', status=401)
            response['WWW-Authenticate'] = 'Basic realm="Grad Slate Sync"'
            return response
        
        # Decode the Authorization header
        try:
            auth_header = request.META['HTTP_AUTHORIZATION']
            auth_parts = auth_header.split()
            
            # Ensure it's a Basic auth header
            if len(auth_parts) != 2 or auth_parts[0].lower() != 'basic':
                return HttpResponse('Unauthorized', status=401)
            
            # Decode credentials
            decoded = base64.b64decode(auth_parts[1]).decode('utf-8')
            username, password = decoded.split(':', 1)
            
            # Check against environment variables
            if (username != API_USERNAME or password != API_PASSWORD):
                return HttpResponse('Invalid credentials', status=401)
        
        except Exception as e:
            return HttpResponse('Unauthorized', status=401)
        
        # Call the view
        return view_func(request, *args, **kwargs)
    
    return wrapper

@csrf_exempt
@basic_auth_required
@require_http_methods(["POST"])
def update_slate(request):
    try:
        # Parse request body
        data = json.loads(request.body)
        
        # Extract parameters
        slate_guid = data.get('SlateGuid')
        bu_id = data.get('BUID')

        # Validate input
        if not slate_guid or not bu_id:
            return JsonResponse({'error': 'SlateGuid and BUID are required'}, status=400)

        if len(slate_guid) > 20 or len(bu_id) > 20:
            return JsonResponse({'error': 'SlateGuid and BUID must be 20 characters or less'}, status=400)

        # Create Slate record
        slate = Slate.objects.create(
            slate_guid=slate_guid,
            bu_id=bu_id
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Slate updated',
            'slate_guid': slate.slate_guid,
            'bu_id': slate.bu_id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
