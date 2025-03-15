import requests
from django.http import HttpRequest
from django.shortcuts import render
from http import HTTPStatus
import json
from datetime import datetime
import re

from .data import Location, EventCategory

def _google_map_url(address: str):
    return  f"https://www.google.com/maps/search/?api=1&query={address}"


def _api_process(
        request: HttpRequest, event_category_req: int, location_req: str, date_req: str):
    response = requests.get(
        url="https://cloud.culture.tw/frontsite/trans/SearchShowAction.do",
        params={"method": "doFindTypeJ", "category": event_category_req}
    )

    if response.status_code == HTTPStatus.OK:
        resp = response.json()

        final_result = []

        for result in resp:
            show_info = result['showInfo']
            title = result['title']

            for show in show_info:
                if location_req in show['location'] and date_req in show['time']:

                    event = {
                        "Time": show.get('time'),
                        "Title": title,
                        "Location": show.get('location'),
                        "GoogleMap": str(_google_map_url(address=show.get('location'))),
                        "LocationName": show.get('locationName'),
                        "OnSales": show.get('onSales'),
                        "Price": show.get('price'),
                        "Latitude": show.get('latitude'),
                        "Longitude": show.get('longitude'),
                        "EndTime": show.get('endTime')
                    }
                    final_result.append(event)

        final_result = sorted(
            final_result,
            key=lambda x: datetime.strptime(x['Time'], '%Y/%m/%d %H:%M:%S'),
            reverse=False,
        )


        json_data = json.dumps(final_result, ensure_ascii=False, indent=4)
        print(json_data)
        return json_data
    return []




def index(request):

    final_resp_data = None
    if request.method == "POST":
        event_category_req = request.POST.get('category_req')
        location_req = request.POST.get('location_req')
        date_req = request.POST.get('date_req')

        if event_category_req and location_req and date_req:
            final_resp_data = _api_process(
                request=request,
                event_category_req=event_category_req,
                location_req=location_req,
                date_req=date_req
            )

    return render(
        request=request,
        template_name='culture.html',
        context={
            'location_json': Location.location_json,
            'event_category_json': EventCategory.event_catetory_json,
            'final_resp_data': json.loads(final_resp_data) if final_resp_data else []
        }
    )
