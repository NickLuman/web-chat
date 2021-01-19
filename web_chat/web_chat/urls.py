from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
]