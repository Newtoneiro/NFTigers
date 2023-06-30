from django.test import TestCase

from auctions.models import Nft, NftCategory, SchoolClass
from auctions.blockchain import Block

from datetime import datetime, timezone

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing


class BlockchainApiViewTest(TestCase):
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
            start_date=start_date,
            end_date=end_date,
            author_name="Tomasz",
            author_surname="Gwiazda",
            current_price=5,
            schoolclass_id=0,
            category_id=0
        )

        Nft.objects.create(
            nft_id='1',
            token="2a7ec83d21f63a9a347ef1505cbff" +
            "0a35498cfdbd3ec13819f7a5825afa848a9",
            start_date=start_date,
            end_date=end_date,
            author_name="Tomasz",
            author_surname="Gwiazda",
            current_price=5,
            schoolclass_id=0,
            category_id=0
        )

    def test_blockchain_create_nft(self):
        mock_datetime = "2023-01-08 17:34:25.235823"
        nft = Nft.objects.get(nft_id=0)
        transactions = [
            (f"NFT {nft.nft_id} created by {nft.author_name} "
             f"{nft.author_surname} was put up for auction at {mock_datetime}")
        ]
        previous_block_hash = None
        block = Block(transactions, previous_block_hash)

        self.assertEqual(block.get_hash(),
                         "2a7ec83d21f63a9a347ef1505cbff0a35498" +
                         "cfdbd3ec13819f7a5825afa848a9")

    def test_block_is_valid(self):
        mock_datetime = "2023-01-08 17:34:25.235823"
        nft = Nft.objects.get(nft_id=0)
        transactions = [
            (f"NFT {nft.nft_id} created by {nft.author_name} "
             f"{nft.author_surname} was put up for auction at {mock_datetime}")
        ]
        previous_block_hash = None
        block = Block(transactions, previous_block_hash)

        self.assertTrue(block.is_valid())

    def test_block_is_invalid(self):
        mock_datetime = "2023-01-08 17:34:25.235823"
        nft = Nft.objects.get(nft_id=0)
        transactions = [
            (f"NFT {nft.nft_id} created by {nft.author_name} "
             f"{nft.author_surname} was put up for auction at {mock_datetime}")
        ]
        previous_block_hash = None
        block = Block(transactions, previous_block_hash)
        block.hash = "Invalid hash"

        self.assertFalse(block.is_valid())

    def test_blockchain_make_bid(self):
        mock_datetime = "2023-01-08 17:56:25.235823"
        nft = Nft.objects.get(nft_id=1)
        self.assertEqual(nft.token, "2a7ec83d21f63a9a347ef1505cbff0a35498" +
                         "cfdbd3ec13819f7a5825afa848a9")

        transactions = [
            f"NFT {nft.nft_id} was bid up by user 1 "
            f"to 10 at {mock_datetime}"
        ]
        previous_block_hash = nft.token
        block = Block(transactions, previous_block_hash)

        self.assertEqual(block.get_hash(),
                         "08aba0eddec8ba9f7c7b3df165dbea43" +
                         "31832ea06d4a51de6b6d69eca0bfae69")
