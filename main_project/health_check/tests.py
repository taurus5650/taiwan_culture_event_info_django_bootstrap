import pytest
from http import HTTPStatus
from unittest.mock import patch, MagicMock

from django.http import HttpRequest
from django.test import TestCase, RequestFactory

from utility import RespCommonResultCode
from health_check.views import index


class TestHealthCheckViews(TestCase):

    def setUp(self):
        """ Initial TestCase. """
        self.factory = RequestFactory()

    @patch('requests.get')
    def test_index_success(self, mock_get):
        request = self.factory.get('/')
        response = index(request)
        assert response.content is not None
