from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from datetime import datetime, timezone
import base64

from auctions.models import Nft
from auctions.models import Bid
from users.models import User
from users.wallet import change_user_wallet

from auctions.blockchain import Block


class AuctionsApiView(APIView):
    '''Class provides API to manage auctions'''

    def get(self, request, format=None, *args, **kwargs):
        '''Returns list of all active or future auctions'''

        now = datetime.now(tz=timezone.utc)
        nfts = Nft.objects.filter(end_date__gt=now)
        nfts = nfts.values()

        if 'category' in self.request.query_params.keys():
            category = self.request.query_params['category']
            try:
                nfts = nfts.filter(category_id=category)
            except Exception:
                return Response(
                    'There is no such category',
                    status=status.HTTP_400_BAD_REQUEST
                )

        if 'class' in self.request.query_params.keys():
            schoolclass = self.request.query_params['class']
            try:
                nfts = nfts.filter(schoolclass_id=schoolclass)
            except Exception:
                return Response(
                    'There is no such class',
                    status=status.HTTP_400_BAD_REQUEST
                )

        for nft in nfts:
            nft['graphic'] = base64.b64encode(nft['graphic']).decode()

        return Response(nfts)

    def post(self, request, format=None):
        '''Places a bid'''

        user_id = str(request.data['usId'])
        nft_id = str(request.data['nftId'])
        bid = int(request.data['bid'])

        # check if auction is active
        nft = Nft.objects.get(nft_id=nft_id)
        now = datetime.now(tz=timezone.utc)
        start_date = nft.start_date
        end_date = nft.end_date
        if start_date < now and end_date > now:
            pass
        else:
            return Response(
                'Auction is not active (not started or ended)',
                status=status.HTTP_400_BAD_REQUEST
            )

        # check if proposed bid is valid
        if bid >= nft.current_price + 1:
            pass
        else:
            return Response(
                'Bid is too low',
                status=status.HTTP_400_BAD_REQUEST
            )

        # check if user has enough funds
        user = User.objects.get(user_id=user_id)
        try:
            change_user_wallet(user, -bid)
            user.save()
        except ValueError:
            return Response(
                'Not enough funds',
                status=status.HTTP_400_BAD_REQUEST
            )

        # create bid
        Bid.objects.create(
            date=datetime.now(tz=timezone.utc),
            price=bid,
            user=user,
            nft=Nft.objects.get(nft_id=nft_id)
        )

        # detach previous user and attach new user
        previous_user = nft.user
        if previous_user is not None:
            previous_bid = nft.current_price
            change_user_wallet(previous_user, previous_bid)
            previous_user.save()
        nft.current_price = bid
        nft.user = user

        current_datetime = datetime.now(tz=timezone.utc)
        transactions = [
            f'NFT {nft.nft_id} was bid up by user {user_id} '
            f'to {bid} at {current_datetime}'
        ]
        previous_block_hash = nft.token
        block = Block(transactions, previous_block_hash)

        nft.token = block.get_hash()

        nft.save()
        return Response("Bid created", status=status.HTTP_201_CREATED)
