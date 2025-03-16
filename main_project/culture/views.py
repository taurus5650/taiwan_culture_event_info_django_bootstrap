from doctest import UnexpectedException

import requests
from django.http import HttpRequest
from django.shortcuts import render
from http import HTTPStatus
import json
from datetime import datetime
import re
from utility import resp_spec, RespCommonResultCode, RespCommonMsg, logger, log_class, log_func, set_request_id, get_request_id

from .data import Location, EventCategory


def _google_map_url(address: str):
    return f"https://www.google.com/maps/search/?api=1&query={address}"


def _google_search(keyword: str):
    return f"https://www.google.com/search?q={keyword}"


@log_func
def _culture_info_process(
        request: HttpRequest, event_category_req: int, location_req: str, date_req: str):
    response = requests.get(
        url="https://cloud.culture.tw/frontsite/trans/SearchShowAction.do",
        params={"method": "doFindTypeJ", "category": event_category_req}
    )

    if response.status_code == HTTPStatus.OK:
        try:
            if not response.text.strip():
                logger.warning(f"Resp Text Empty: {response.text}")
                return resp_spec(
                    result=RespCommonResultCode.UNKNOWN_ERROR,
                    message=RespCommonMsg.UNKNOWN_ERROR,
                    result_obj="Empty response."
                )

            resp = response.json()
        except ValueError as e:
            logger.error(f"Error Parsing JSON: {e}")
            return resp_spec(
                result=RespCommonResultCode.FAILED,
                message=RespCommonMsg.FAILED,
                result_obj=f"ValueError: {e}"
            )

        final_result = []

        for result in resp:
            show_info = result.get('showInfo', [])
            title = result.get('title', 'Untitled')

            for show in show_info:
                if location_req in show['location'] and date_req in show['time']:
                    event = {
                        "Time": show.get('time'),
                        "Title": title,
                        "GoogleSearch": str(_google_search(keyword=title)),
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
            key=lambda x: datetime.strptime(
                x['Time'], '%Y/%m/%d %H:%M:%S'),
            reverse=False,
        )

        return resp_spec(
            result=RespCommonResultCode.SUCCESS,
            message=RespCommonMsg.SUCESS,
            result_obj=final_result
        )

    logger.error(f"Request Failed with Status Code: {response.status_code}")
    return resp_spec(
        result=RespCommonResultCode.FAILED,
        message=RespCommonMsg.FAILED,
        result_obj=(f"Request Failed with Status Code: {response.status_code}")
    )

@log_func
def index(request):
    final_resp_data = None
    if request.method == "POST":
        event_category_req = request.POST.get('category_req')
        location_req = request.POST.get('location_req')
        date_req = request.POST.get('date_req')
        logger.info(f"WebRequest: {event_category_req}, {location_req}, {date_req}")


        if event_category_req and location_req and date_req:
            final_resp_data = _culture_info_process(
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
            'final_resp_data': final_resp_data['ResultObject'] if final_resp_data else []
        }
    )
