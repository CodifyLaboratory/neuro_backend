from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dev-admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/', include('eegtest.urls')),
    # path('api/', include('medicine.urls')),
]
