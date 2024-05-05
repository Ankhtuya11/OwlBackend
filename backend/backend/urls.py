
from django.contrib import admin
from django.urls import path
from backendApp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', registerUser),
    path('login/', loginUser),
    path('addmovie/', addMovie),
    path('bookadd/', bookadd),
    path('checkService/', checkService),
    path('b64ToText/', b64Text),
]
