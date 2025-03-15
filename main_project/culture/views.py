from django.shortcuts import render
from .data import Location, EventCategory
import requests


def _api_process(request, event_category):
    response = requests.get(
        url="https://cloud.culture.tw/frontsite/trans/SearchShowAction.do",
        params={"method": "doFindTypeJ", "category": event_category}
    )
    resp = response.json()
    print(resp)

def index(request):
    event_category = request.GET.get('category_req', '')

    if event_category:
        _api_process(request, event_category)
        
    return render(
        request=request,
        template_name='culture.html',
        context={
            'location_json': Location.location_json,
            'event_category_json': EventCategory.event_catetory_json
        }
    )
