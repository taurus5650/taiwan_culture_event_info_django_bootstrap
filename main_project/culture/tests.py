import pytest
from http import HTTPStatus
from unittest.mock import patch, MagicMock

from django.http import HttpRequest
from django.test import TestCase, RequestFactory

from utility import RespCommonResultCode
from culture.views import _culture_info_process, index


class TestCulcureViews(TestCase):

    def setUp(self):
        """ Initial TestCase. """
        self.factory = RequestFactory()

    @patch('requests.get')
    def test_culture_info_process_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "showInfo": [{
                    "location": "臺北市",
                    "time": "2025/11/01 10:00:00",
                    "locationName": "模擬音樂廳1",
                    "onSales": "2023/10/01",
                    "price": "500",
                    "latitude": "25.0314",
                    "longitude": "121.5647",
                    "endTime": "2023/11/30 23:59:59"
                }],
                "title": "模擬音樂會1"
            },
            {
                "showInfo": [{
                    "location": "臺北市",
                    "time": "2025/11/02 10:00:00",
                    "locationName": "模擬音樂廳2",
                    "onSales": "2023/10/02",
                    "price": "600",
                    "latitude": "25.0314",
                    "longitude": "121.5647",
                    "endTime": "2023/11/30 23:59:59"
                }],
                "title": "模擬音樂會2"
            }
        ]
        mock_get.return_value = mock_response

        resp = _culture_info_process(
            request=HttpRequest(),
            event_category_req=3,
            location_req="臺北",
            date_req="2025/11"
        )

        assert resp['Result'] == RespCommonResultCode.SUCCESS
        assert resp['ResultObject'] is not None
        assert resp['ResultObject'][0]['Title'] == "模擬音樂會1"

    @patch('requests.get')
    def test_culture_info_process_null_str(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_get.return_value = mock_response

        resp = _culture_info_process(
            request=HttpRequest(),
            event_category_req=3,
            location_req="新北市",
            date_req="2025/11"
        )

        assert resp['Result'] == RespCommonResultCode.UNKNOWN_ERROR

    def test_index_get_request(self):
        request = self.factory.get('/')
        response = index(request)
        assert response.status_code == HTTPStatus.OK

    @patch('requests.get')
    def test_index_post_missing_parameters(self, mock_get):
        data = {
            "invalid_param": "value"
        }
        request = self.factory.post('/', data=data)
        response = index(request)
        assert response.status_code == HTTPStatus.OK
