from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# Here include all necessary views (Admin and app(s)... )
urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
