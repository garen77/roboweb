from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('move', views.move),
    path('heartBeat', views.heartBeat),
    path('recognize', views.recognize),
]
