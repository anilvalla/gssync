import traceback
import logging
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

logger = logging.getLogger(__name__)

def home_page(request):
    try:
        projects = Project.objects.all()
        return render(request, 'home.html', {'projects': projects})
    except Exception as e:
        # Log the full traceback
        logger.error("Error in home_page view", exc_info=True)
        
        # Return a detailed error response
        error_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
        return HttpResponse(error_message, status=500)

class HomeAPIView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to the Project Management API',
            'available_endpoints': [
                '/api/projects/',
                '/api/tasks/'
            ]
        })

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer