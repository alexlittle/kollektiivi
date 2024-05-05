from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from django.conf.urls.i18n import i18n_patterns
    
from kollektiivi.views import HomeView, PageView, MembersView, MemberProfileView

app_name = 'kollektiivi'

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('i18n/', include('django.conf.urls.i18n'))
    ]

urlpatterns += i18n_patterns(
    path('', HomeView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('jäseniä/', MembersView.as_view(), name="members"),
    path('jäseniä/<str:slug>/', MemberProfileView.as_view(), name="member_profile"),
    path('uutiset/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('<str:slug>/', PageView.as_view(), name="page"),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
