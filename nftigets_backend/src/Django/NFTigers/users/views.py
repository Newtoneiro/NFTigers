from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from rest_framework import status
from users.wallet import change_user_wallet


class WalletApiView(APIView):
    """Class provides API to manage user's wallet"""

    def post(self, request, format=None):
        """Returns user wallet state"""

        user_id = request.data["usId"]
        try:
            user = User.objects.get(user_id=user_id)
        except Exception:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        data = {"mail": user.mail, "wallet": user.money}
        return Response(data)

    def put(self, request, format=None):
        """Adds money to user wallet"""

        user_id = request.data["usId"]
        try:
            user = User.objects.get(user_id=user_id)
        except Exception:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        income = request.data["income"]
        change_user_wallet(user, income)
        return Response("Wallet updated", status=status.HTTP_202_ACCEPTED)


class UsersApiView(APIView):
    """Class provides API to manage users in our database"""

    def post(self, request, format=None):
        """Registers user in our database"""

        requested_user_id = request.data["usId"]

        # check if ID is already used
        used_ids = [
            user.user_id for user in User.objects.all()
        ]
        if requested_user_id in used_ids:
            return Response(
                "ID already used", status=status.HTTP_400_BAD_REQUEST
            )

        # create user
        User.objects.create(
            user_id=requested_user_id,
            # name=request.data["name"],
            # surname=request.data["surname"],
            mail=request.data["email"],
            money=0,
            is_admin=False
        )

        return Response("User created", status=status.HTTP_201_CREATED)
