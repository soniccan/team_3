from django.urls import path
from . import views

app_name = 'itsumoku'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('form',views.form, name ='form'),
    path('result',views.result, name ='result')
]