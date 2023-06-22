from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from kollektiivi.views import HomeView, PageView, TagView

app_name = 'kollektiivi'

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', HomeView.as_view(), name="home"),
    path('tag/<str:slug>/', TagView.as_view(), name="tag"),
    path('admin/', admin.site.urls),
    path('<str:slug>/', PageView.as_view(), name="page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
