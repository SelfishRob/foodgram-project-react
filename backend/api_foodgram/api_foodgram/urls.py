from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
]
