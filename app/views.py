from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

# Existing ViewSets (keep these)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# New views for homepage and API root
def home_page(request):
    projects = Project.objects.all()
    return render(request, 'home.html', {'projects': projects})

class HomeAPIView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to the Project Management API',
            'available_endpoints': [
                '/api/projects/',
                '/api/tasks/'
            ]
        })
