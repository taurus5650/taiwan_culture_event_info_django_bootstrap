from unittest.mock import patch

from django.test import TestCase, RequestFactory

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
