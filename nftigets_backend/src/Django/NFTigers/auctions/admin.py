from django.contrib import admin

from .models import BinaryFileInput, Nft, NftCategory, SchoolClass

from auctions.blockchain import Block

from django.db import models
from datetime import datetime, timezone


class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        'nft_id',
        'token',
        'author_name',
        'author_surname',
        'img_preview',
        'start_date',
        'end_date',
        'current_price',
        'category',
        'schoolclass',
        'user',
    )

    formfield_overrides = {
        models.BinaryField: {'widget': BinaryFileInput()},
    }

    readonly_fields = ['img_preview']

    def save_model(self, request, obj, form, change):
        current_datetime = datetime.now(tz=timezone.utc)
        transactions = [f"NFT {obj.nft_id} created by {obj.author_name} "
                        f"{obj.author_surname} was put up for "
                        f"auction at {current_datetime}"]
        previous_block_hash = None
        block = Block(transactions, previous_block_hash)

        obj.token = block.get_hash()
        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category_id',
        'name',
    )


class ClassAdmin(admin.ModelAdmin):
    list_display = (
        'schoolclass_id',
        'name',
        'start_year',
    )


admin.site.register(Nft, AuctionAdmin)
admin.site.register(NftCategory, CategoryAdmin)
admin.site.register(SchoolClass, ClassAdmin)
