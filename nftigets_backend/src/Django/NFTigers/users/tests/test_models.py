from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(user_id="0", mail="a@a.a")

    def test_str(self):
        user = User.objects.get(user_id="0")
        self.assertEqual(str(user), 'a@a.a')
