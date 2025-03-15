from django.urls import path
from . import views


urlpatterns = [
    path('tech_stack/', views.index, name='tech_stack'),
]