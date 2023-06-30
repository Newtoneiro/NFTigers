from base64 import b64encode
from django import forms
from django.db import models
from django.utils.html import mark_safe
from users.models import User, VarCharField


class NftCategory(models.Model):
    category_id = models.AutoField(
        primary_key=True)

    name = VarCharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "CATEGORIES"


class SchoolClass(models.Model):
    schoolclass_id = models.AutoField(primary_key=True)

    name = VarCharField(max_length=2)
    start_year = models.IntegerField()

    def __str__(self):
        return str(self.start_year) + " - " + self.name

    class Meta:
        db_table = "SCHOOLCLASSES"
        unique_together = ('name', 'start_year',)


class Nft(models.Model):
    nft_id = models.AutoField(primary_key=True)
    token = VarCharField(max_length=100, null=True,
                         editable=False, unique=True)
    author_name = VarCharField(max_length=15)
    author_surname = VarCharField(max_length=20)
    graphic = models.BinaryField(editable=True, max_length=1000000)

    def img_preview(self):
        encode = b64encode(self.graphic).decode()
        return mark_safe(
            f'<img src="data:image/jpeg;base64,{encode}" class="img-thumbnail" width = "300"/>'
        )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    current_price = models.DecimalField(max_digits=6, decimal_places=2)

    category = models.ForeignKey(
        NftCategory, on_delete=models.DO_NOTHING, blank=False, null=True,
    )
    schoolclass = models.ForeignKey(
        SchoolClass, on_delete=models.DO_NOTHING, blank=False, null=False
    )
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
        blank=True, null=True, editable=False
    )

    class Meta:
        db_table = "SCHOOLWORKS"


class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)

    date = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_winner = models.BooleanField(default=False)
    date_winner = models.DateTimeField(null=True)

    user = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    nft = models.ForeignKey(
        Nft, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        db_table = "BIDS"


class BinaryFileInput(forms.ClearableFileInput):
    def is_initial(self, value):
        return bool(value)

    def format_value(self, value):
        if self.is_initial(value):
            return f'{len(value)} bytes'

    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        if upload:
            binary_file_data = upload.read()
            image_data = b64encode(binary_file_data).decode('utf-8')
            return image_data
