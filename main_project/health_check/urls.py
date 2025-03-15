from django.urls import path
from . import views


urlpatterns = [
    path('health_check/', views.index, name='health_check'),
    path('health_check/html/', views.html_index, name='health_check_html'),
]