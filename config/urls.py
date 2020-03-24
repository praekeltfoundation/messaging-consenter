from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('consent/', include('consenter.urls')),
    path('admin/', admin.site.urls),
]
