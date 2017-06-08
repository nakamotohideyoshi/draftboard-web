#
# promocode/admin.py

from django.contrib import admin

from promocode.models import Promotion, PromoCode

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):

    list_display = ['enabled','code','first_deposit_only','description',
                    'expires','max_bonuscash','fpp_per_bonus_dollar','admin_notes']
    list_display_links = ['code']
    list_editable = ['enabled','description','admin_notes']

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):

    list_display = ['user','promotion']

