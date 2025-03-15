from django.urls import path
from . import views


urlpatterns = [
    path('culture/', views.index, name='culture'),
]