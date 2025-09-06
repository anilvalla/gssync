from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Slate

def home_page(request):
    try:
        return render(request, 'home.html')
    except Exception as e:
        print(f"Error rendering home page: {e}")
        return HttpResponse(f"An error occurred: {e}", status=500)

@csrf_exempt
def update_slate(request):
    if request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.body:
                data = json.loads(request.body)
            else:
                data = request.POST

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
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Error in UpdateSlate: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
