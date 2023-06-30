from django.test import TestCase
import decimal
from users.wallet import change_user_wallet


class WalletTest(TestCase):
    class User:
        money = decimal.Decimal(0)
        def save(self):
            pass
        
    def test_change_user_wallet(self):
        user = self.User()
        self.assertEqual(user.money, decimal.Decimal(0))
        
        change_user_wallet(user, 5)
        self.assertEqual(user.money, decimal.Decimal(5))
        
    def test_change_user_wallet_user_has_no_money(self):
        user = self.User()
        self.assertEqual(user.money, decimal.Decimal(0))
        
        with self.assertRaises(ValueError):
            change_user_wallet(user, -5)
        