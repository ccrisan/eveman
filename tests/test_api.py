from datetime import datetime
from typing import Optional

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from api.models import Event
from api.serializers import ViewEventSerializer


class APITestCase(TestCase):
    TEST_USERNAME = "user1"
    TEST_PASSWORD = "deadbeef"

    def __init__(self, *args, **kwargs):
        self._test_user: Optional[User] = None
        super().__init__(*args, **kwargs)

    def get_test_user(self) -> User:
        if not self._test_user:
            self._test_user = User.objects.create_user(
                username=self.TEST_USERNAME,
                password=self.TEST_PASSWORD,
            )

        return self._test_user

    def get_auth_headers(self):
        self.get_test_user()  # Ensure user is created
        response = self.client.post(reverse("token"), {"username": self.TEST_USERNAME, "password": self.TEST_PASSWORD})
        access_token = response.data["access"]
        return {"Authorization": f"Bearer {access_token}"}


class TokenTestCase(APITestCase):
    def test_access(self):
        self.get_test_user()  # Ensure user is created
        response = self.client.post(reverse("token"), {"username": self.TEST_USERNAME, "password": self.TEST_PASSWORD})
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_access_invalid(self):
        self.get_test_user()  # Ensure user is created
        response = self.client.post(reverse("token"), {"username": self.TEST_USERNAME, "password": "invalid"})
        assert response.status_code == 401

    def test_refresh(self):
        self.get_test_user()  # Ensure user is created

        # Obtain access/refresh tokens
        response = self.client.post(reverse("token"), {"username": self.TEST_USERNAME, "password": self.TEST_PASSWORD})
        refresh_token = response.data["refresh"]

        # Refresh token
        response = self.client.post(reverse("token_refresh"), {"refresh": refresh_token})
        assert response.status_code == 200
        assert 'access' in response.data

    def test_refresh_invalid(self):
        self.get_test_user()  # Ensure user is created

        # Refresh token
        response = self.client.post(reverse("token_refresh"), {"refresh": "invalid"})
        assert response.status_code == 401


class GetAllEventsTest(APITestCase):
    def setUp(self):
        user = self.get_test_user()
        Event.objects.create(
            name="event1",
            description="description1",
            moment=datetime(2021, 1, 2, 3, 4, 5),
            created_by=user,
        )
        Event.objects.create(
            name="event2",
            description="description2",
            moment=datetime(2022, 1, 2, 3, 4, 5),
            created_by=user,
        )

    def test_get_all_events(self):
        auth_headers = self.get_auth_headers()
        response = self.client.get(reverse("events"), headers=auth_headers)
        events = Event.objects.all()
        serializer = ViewEventSerializer(events, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
