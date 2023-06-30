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


class AuctionsApiViewTest(TestCase):
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
            '01/01/22', '%d/%m/%y'
        ).replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(
            '02/01/22', '%d/%m/%y'
        ).replace(tzinfo=timezone.utc)

        Nft.objects.create(
            nft_id='0',
            token='fake token 1',
            start_date=start_date,
            end_date=end_date,
            current_price=5,
            schoolclass_id=0,
            category_id=0
        )

        start_date = datetime.strptime(
            '01/01/23', '%d/%m/%y'
        ).replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(
            '30/01/23', '%d/%m/%y'
        ).replace(tzinfo=timezone.utc)

        Nft.objects.create(
            nft_id='1',
            token='fake token 2',
            start_date=start_date,
            end_date=end_date,
            current_price=5,
            schoolclass_id=0,
            category_id=0
        )

        # Users
        User.objects.create(user_id="old", mail="a", money=100)
        User.objects.create(user_id='new', mail="b", money=100)

    @mock.patch('auctions.views.datetime')
    def test_get(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK

        response = self.client.get('/api/auctions/')

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)

    @mock.patch('auctions.views.datetime')
    def test_get_with_class(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK

        response = self.client.get('/api/auctions/?class=0')

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)

    @mock.patch('auctions.views.datetime')
    def test_get_with_class_invalid(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK

        response = self.client.get('/api/auctions/?class=invalid')

        self.assertEqual(response.status_code, 400)

    @mock.patch('auctions.views.datetime')
    def test_get_with_category(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK

        response = self.client.get('/api/auctions/?category=1')

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 0)

    @mock.patch('auctions.views.datetime')
    def test_get_with_category_invalid_data(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK

        response = self.client.get('/api/auctions/?category=invalid_data')

        self.assertEqual(response.status_code, 400)

    @mock.patch('auctions.views.datetime')
    def test_post_success(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK

        response = self.client.post(
            '/api/auctions/',
            {
                'usId': 'old',
                'nftId': 1,
                'bid': 10
            }
        )

        nft = Nft.objects.get(nft_id=1)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(nft.current_price, 10)
        self.assertEqual(nft.user.user_id, 'old')

        response = self.client.post(
            '/api/auctions/',
            {
                'usId': 'new',
                'nftId': 1,
                'bid': 15
            }
        )

        nft = Nft.objects.get(nft_id=1)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(nft.current_price, 15)
        self.assertEqual(nft.user.user_id, 'new')

    @mock.patch('auctions.views.datetime')
    def test_post_inactive_auction(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK

        response = self.client.post(
            '/api/auctions/',
            {
                'usId': 'new',
                'nftId': 0,
                'bid': 10
            }
        )
        self.assertEqual(response.status_code, 400)

    @mock.patch('auctions.views.datetime')
    def test_post_invalid_bid(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK

        response = self.client.post(
            '/api/auctions/',
            {
                'usId': 'new',
                'nftId': 1,
                'bid': 5
            }
        )
        self.assertEqual(response.status_code, 400)

    @mock.patch('auctions.views.datetime')
    def test_post_no_funds(self, mock_datetime):
        mock_datetime.now.return_value = DATETIME_MOCK

        response = self.client.post(
            '/api/auctions/',
            {
                'usId': 'new',
                'nftId': 1,
                'bid': 99999
            }
        )
        self.assertEqual(response.status_code, 400)
