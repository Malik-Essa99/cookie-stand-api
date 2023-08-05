from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Cookie

class CookieTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()
        testuser2 = get_user_model().objects.create_user(
            username="testuser2", password="pass2"
        )
        testuser2.save()

        test_cookie = Cookie.objects.create(
            location="kitchen",
            owner=testuser1,
            description="Delicious cookies baked with love.",
        )
        test_cookie.save()

    def setUp(self) -> None:
        self.client.login(username="testuser1", password="pass")

    def test_cookie_model(self):
        cookie = Cookie.objects.get(id=1)
        actual_owner = str(cookie.owner)
        actual_location = str(cookie.location)
        actual_description = str(cookie.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_location, "kitchen")
        self.assertEqual(
            actual_description, "Delicious cookies baked with love."
        )

    def test_get_cookie_list(self):
        url = reverse("cookie_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookies = response.data
        self.assertEqual(len(cookies), 1)
        self.assertEqual(cookies[0]["location"], "kitchen")

    def test_auth_required(self):
        self.client.logout()
        url = reverse("cookie_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_owner_can_delete_cookie(self):
        self.client.logout()
        self.client.login(username="testuser2", password="pass2")
        url = reverse("cookie_detail", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
