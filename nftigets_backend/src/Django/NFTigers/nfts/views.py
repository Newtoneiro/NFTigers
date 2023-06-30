from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from auctions.models import Nft, NftCategory, SchoolClass

import base64


class CategoriesApiView(APIView):
    '''Class provides API to read nfts categories'''

    def get(self, request, format=None):
        '''Returns list of all categories'''
        return Response(NftCategory.objects.all().values())


class SchoolClassApiView(APIView):
    '''Class provides API to read school classes'''

    def get(self, request, format=None):
        '''Returns list of all school classes'''
        return Response(SchoolClass.objects.all().values())


class NftsApiView(APIView):
    """Class provides API to manage user's nfts"""

    def post(self, request, format=None):
        """Returns list of NFTs belonging to user with given ID"""

        current_user_id = str(request.data["usId"])
        now = datetime.now()
        user_nfts = []

        for nft in Nft.objects.filter(end_date__lt=now).values():
            if "user_id" in nft:
                if nft["user_id"] == current_user_id:
                    graphic = base64.b64encode(nft["graphic"]).decode()

                    nft_data = {
                        "nft_id": nft["nft_id"],
                        "author_name": nft["author_name"],
                        "author_surname": nft["author_surname"],
                        "graphic": graphic,
                        "current_price": nft["current_price"],
                        "end_date": nft["end_date"]
                    }

                    user_nfts.append(nft_data)

        return Response(user_nfts)
