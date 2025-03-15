from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('culture/', views.index, name='culture'),
    path('', RedirectView.as_view(url='/culture/', permanent=False)), # Rzoot path direct to /culture
]
