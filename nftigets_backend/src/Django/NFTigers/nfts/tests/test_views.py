from django.test import TestCase

from auctions.models import Nft, NftCategory, SchoolClass
from users.models import User

from datetime import datetime, timezone
from unittest import mock
import json


# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

DATETIME_MOCK = datetime.strptime(
    '15/01/23', '%d/%m/%y'
).replace(tzinfo=timezone.utc)


class NFTSFinishedApiViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SchoolClass.objects.create(
            schoolclass_id=0,
            name='A',
            start_year=2001
        )

        NftCategory.objects.create(
            category_id=0,
            name="test_category"
        )
        # NFTs
        start_date = datetime.strptime(
            '01/01/23', '%d/%m/%y'
        ).replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(
            '06/01/23', '%d/%m/%y'
        ).replace(tzinfo=timezone.utc)

        # User
        nft_user_1 = User.objects.create(user_id='0', mail="0")
        nft_user_2 = User.objects.create(user_id='1', mail="1")

        Nft.objects.create(
            nft_id='0',
            token='fake token 0',
            start_date=start_date,
            end_date=end_date,
            current_price=10,
            user=nft_user_1,
            schoolclass_id=0,
            category_id=0
        )

        Nft.objects.create(
            nft_id='1',
            token='fake token 1',
            start_date=start_date,
            end_date=end_date,
            current_price=10,
            user=nft_user_2,
            schoolclass_id=0,
            category_id=0
        )

        Nft.objects.create(
            nft_id='2',
            token='fake token 2',
            start_date=start_date,
            end_date=end_date,
            current_price=10,
            user=nft_user_2,
            schoolclass_id=0,
            category_id=0
        )

    @mock.patch('nfts.views.datetime')
    def test_nft_first_user(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK
        response = self.client.post(
            '/api/nfts/',
            {
                'usId': '0',
            }
        )

        json_value = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_value), 1)
        self.assertEqual(json_value[0]['nft_id'], 0)

    @mock.patch('nfts.views.datetime')
    def test_nft_second_user(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK
        response = self.client.post(
            '/api/nfts/',
            {
                'usId': '1',
            }
        )

        json_value = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_value), 2)


class NFTSNotFinishedApiViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        NftCategory.objects.create(
            category_id=0,
            name="test_category"
        )

        NftCategory.objects.create(
            category_id=1,
            name="test_category_2"
        )

        SchoolClass.objects.create(
            schoolclass_id=1,
            name='B',
            start_year=2002
        )

        SchoolClass.objects.create(
            schoolclass_id=0,
            name='A',
            start_year=2001
        )

        # NFTs
        start_date = datetime.strptime(
            '01/01/23', '%d/%m/%y'
        ).replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(
            '30/01/23', '%d/%m/%y'
        ).replace(tzinfo=timezone.utc)

        # User
        nft_user_1 = User.objects.create(user_id='0', mail="0")
        nft_user_2 = User.objects.create(user_id='1', mail="1")

        Nft.objects.create(
            nft_id='0',
            token='fake token',
            start_date=start_date,
            end_date=end_date,
            current_price=10,
            user=nft_user_1,
            schoolclass_id=0,
            category_id = 0
        )

        Nft.objects.create(
            nft_id='1',
            token='fake token 1',
            start_date=start_date,
            end_date=end_date,
            current_price=10,
            user=nft_user_2,
            schoolclass_id=0,
            category_id = 0

        )

        Nft.objects.create(
            nft_id='2',
            token='fake token 2',
            start_date=start_date,
            end_date=end_date,
            current_price=10,
            user=nft_user_2,
            schoolclass_id=0,
            category_id = 0
        )

    @mock.patch('nfts.views.datetime')
    def test_nft_first_user(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK
        response = self.client.post(
            '/api/nfts/',
            {
                'usId': '0',
            }
        )

        json_value = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_value), 0)

    @mock.patch('nfts.views.datetime')
    def test_nft_second_user(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK
        response = self.client.post(
            '/api/nfts/',
            {
                'usId': '1',
            }
        )

        json_value = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_value), 0)

    @mock.patch('nfts.views.datetime')
    def test_nft_get_all_classes(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK
        response = self.client.get(
            '/api/classes/'
        )

        json_value = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_value), 2)

    @mock.patch('nfts.views.datetime')
    def test_nft_get_all_categories(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK
        response = self.client.get(
            '/api/categories/'
        )

        json_value = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_value), 2)
