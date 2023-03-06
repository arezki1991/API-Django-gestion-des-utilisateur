from django.contrib import admin
from django.urls import path, include
from users.views import api_root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/users/', include('users.urls')),
]