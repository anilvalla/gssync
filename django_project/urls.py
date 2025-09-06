from django.contrib import admin
from django.urls import path
from app.views import home_page, update_slate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('UpdateSlate', update_slate, name='update_slate'),
]
