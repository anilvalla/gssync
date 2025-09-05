from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import ProjectViewSet, TaskViewSet, home_page, HomeAPIView

# Create router
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # Home page
    path('', home_page, name='home'),
    
    # Root API view
    path('api/', HomeAPIView.as_view(), name='api_root'),
    
    # API endpoints
    path('api/', include(router.urls)),
]