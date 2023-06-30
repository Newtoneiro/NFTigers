from users.models import User
import decimal


def change_user_wallet(user, change):
    """Changes user wallet

    Args:
        user (User): user to change wallet
        change (int/float/string): money to add

    Raises:
        ValueError: occures when money + change less than zero
    """ 
    if user.money + decimal.Decimal(change) < decimal.Decimal(0):
        raise ValueError()
    user.money += decimal.Decimal(change)
    user.save()
