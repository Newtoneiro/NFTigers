from django.db import models


class VarCharField(models.CharField):
    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super().__init__(
            max_length=max_length, *args, **kwargs)

    def db_type(self, connection):
        if(connection.vendor == 'oracle'):
            return "VARCHAR2(%s CHAR)" % self.max_length
        else:
            return "VARCHAR2(%s)" % self.max_length


class User(models.Model):
    user_id = VarCharField(primary_key=True, max_length=100)

    name = VarCharField(max_length=30, blank=True)
    surname = VarCharField(max_length=30, blank=True)
    mail = VarCharField(max_length=40, unique=True)
    money = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.mail

    class Meta:
        db_table = "USERS"
