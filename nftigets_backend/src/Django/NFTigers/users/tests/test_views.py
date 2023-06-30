from django.test import TestCase

from users.models import User
import json

from datetime import datetime, timezone


class UsersApiViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            user_id="1",
            name="imie",
            surname="nazwisko",
            mail="email@gmail.com"
        )

    def test_view_new_usId_add_user(self):
        request = {"usId": "2", "email": "newemail1@gmail.com",
                   "name": "Jan", "surname": "Kowalski"}
        response = self.client.post('/api/users/', request)
        self.assertEqual(response.status_code, 201)

    def test_view_usId_exists_returns_bad_request(self):
        request = {"usId": "1", "email": "newemail2@gmail.com",
                   "name": "Jan", "surname": "Kowalski"}
        response = self.client.post('/api/users/', request)
        self.assertEqual(response.status_code, 400)


class WalletApiViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            user_id="1",
            name="imie",
            surname="nazwisko",
            mail="email@gmail.com"
        )

    def test_view_get_user_wallet(self):
        request = {"usId": "1"}
        response = self.client.post('/api/wallet/', request)
        self.assertEqual(response.status_code, 200)
        json_value = json.loads(response.content.decode("utf-8"))
        self.assertEqual(json_value["wallet"], 0)

    def test_view_get_user_wallet_user_does_not_exists(self):
        request = {"usId": "2"}
        response = self.client.post('/api/wallet/', request)
        self.assertEqual(response.status_code, 404)

    def test_view_charge_user_wallet(self):
        request = json.dumps({"usId": "1", "income": "5"})
        response = self.client.put(
            '/api/wallet/', request, content_type="application/json"
            )
        self.assertEqual(response.status_code, 202)
        request = {"usId": "1"}
        response = self.client.post('/api/wallet/', request)
        json_value = json.loads(response.content.decode("utf-8"))
        self.assertEqual(json_value["wallet"], 5)

    def test_view_charge_user_wallet_user_does_not_exists(self):
        request = json.dumps({"usId": "2", "income": "5"})
        response = self.client.put(
            '/api/wallet/', request, content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
