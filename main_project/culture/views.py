from django.shortcuts import render
from .data import Location, EventCategory


def process():
    pass

def index(request):
    return render(
        request=request,
        template_name='culture.html',
        context={
            'location_json': Location.location_json,
            'event_category_json': EventCategory.event_catetory_json
        }
    )
