from django.urls import path
from . import views


urlpatterns = [
    path('concert/', views.index, name='concert'),
]