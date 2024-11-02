from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appSElist4.urls')),  # This includes URLs from appSElist4
]
