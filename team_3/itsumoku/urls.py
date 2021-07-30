from django.urls import path
from . import views

app_name = 'itsumoku'
urlpatterns = [
    path('', views.index, name = 'index'),
]