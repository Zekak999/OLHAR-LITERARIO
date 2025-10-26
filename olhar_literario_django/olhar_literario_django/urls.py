"""
URL configuration for olhar_literario_django project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
import os

# View para servir favicon
def favicon_view(request):
    favicon_path = os.path.join(settings.BASE_DIR, 'static', 'favicon.svg')
    if os.path.exists(favicon_path):
        return FileResponse(open(favicon_path, 'rb'), content_type='image/svg+xml')
    return JsonResponse({'error': 'Favicon not found'}, status=404)

# View para servir extra-covers-meta.json
def extra_covers_meta_view(request):
    json_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'extra-covers-meta.json')
    if os.path.exists(json_path):
        return FileResponse(open(json_path, 'rb'), content_type='application/json')
    # Retornar array vazio se não existir
    return JsonResponse([], safe=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', favicon_view, name='favicon'),
    path('images/extra-covers-meta.json', extra_covers_meta_view, name='extra_covers_meta'),
    path('', include('books.urls')),
]

# Servir arquivos de mídia (uploads) - SEMPRE, tanto em dev quanto em produção
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    # Servir arquivos estáticos (CSS, JS, imagens estáticas)
    urlpatterns += [
        re_path(r'^(?P<path>.*\.(css|js|png|jpg|jpeg|gif|svg|ico))$', 
                serve, 
                {'document_root': settings.BASE_DIR.parent}),
    ]
