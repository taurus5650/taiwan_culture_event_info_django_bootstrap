from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestTechStackViews(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('tech_stack'))
        assert response.status_code == HTTPStatus.OK
        assert 'tech_stack.html' in [tmpl.name for tmpl in response.templates]
