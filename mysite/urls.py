
from django.contrib import admin
from django.urls import path, include
#from main.views import index

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
]
