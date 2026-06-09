from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]

# Siempre servir media (whitenoise solo maneja static, no media)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# En desarrollo también servir static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
