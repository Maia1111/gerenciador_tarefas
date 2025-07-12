"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from tasks.views import RegisterView, CustomLoginView
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
import os

def serve_sw(request):
    """
    Serve service worker from static files.
    
    Args:
        request: Requisição HTTP
    
    Returns:
        HttpResponse: Arquivo service worker ou fallback
    """
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    if os.path.exists(sw_path):
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content.encode('utf-8'), content_type='application/javascript')
    return HttpResponse('console.log("Service Worker not found");'.encode('utf-8'), content_type='application/javascript')

def custom_logout(request):
    """
    View customizada para logout que aceita GET e POST.
    Faz logout imediato e redireciona para login.
    
    Args:
        request: Requisição HTTP
    
    Returns:
        HttpResponse: Redirecionamento para página de login
    """
    logout(request)
    return redirect('login')

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('login')), name='home'),
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('sw.js', serve_sw, name='service_worker'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
