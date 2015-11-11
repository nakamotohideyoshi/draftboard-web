#
# optimal_payments/models.py

from django.db import models
from django.contrib.auth.models import User

class Optimal(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=False)
    oid = models.CharField(max_length=256, null=False)

    class Meta:
        abstract = True

class Profile(Optimal):
    # response json from creating a profile:
    # {
    #   "id" : "716adb4f-6b85-4089-ba9c-d9c0eb649cd7",
    #   "status" : "ACTIVE",
    #   "merchantCustomerId" : "mycustomer1",
    #   "locale" : "en_US",
    #   "firstName" : "John",
    #   "lastName" : "Smith",
    #   "phone" : "713-444-5555",
    #   "email" : "john.smith@somedomain.com",
    #   "paymentToken" : "PyhYo1nGKUfWOPj"
    # }

    merchant_customer   = models.CharField(max_length=64, null=False)
    first_name          = models.CharField(max_length=64, null=False)
    last_name           = models.CharField(max_length=64, null=False)
    phone               = models.CharField(max_length=64, null=False)
    email               = models.CharField(max_length=64, null=False)

    payment_token       = models.CharField(max_length=64, null=False)

    class Meta:
        abstract = False

class Address(Optimal):
    # response json from adding an Address to a Profile via Optimal:
    # {
    #   "id" : "81ffcddf-ad82-40d2-aaa0-c4f9c376ad65",
    #   "status" : "ACTIVE",
    #   "street" : "100 Queen Street West",
    #   "city" : "Toronto",
    #   "state" : "ON",
    #   "country" : "CA",
    #   "zip" : "M5H 2N2",
    #   "defaultShippingAddressIndicator" : false
    # }

    street      = models.CharField(max_length=128, null=False)
    city        = models.CharField(max_length=64, null=False)
    state       = models.CharField(max_length=64, null=False)
    country     = models.CharField(max_length=64, null=False)
    zip         = models.CharField(max_length=16, null=False)
    default     = models.BooleanField(default=False, null=False,
                            help_text='whether this address is the default address to use')

    class Meta:
        abstract = False

class Card(Optimal):
    # response json from adding a card:
    # {
    #   "id" : "178ae2b8-85a5-4761-b1dd-4f14ac73571b",
    #   "status" : "ACTIVE",
    #   "holderName" : "John Smith",
    #   "cardBin" : "453091",
    #   "lastDigits" : "2345",
    #   "cardExpiry" : {
    #     "month" : 12,
    #     "year" : 2019
    #   },
    #   "cardType" : "VI",
    #   "paymentToken" : "CaBP0abDKgROjYU",
    #   "billingAddressId" : "81ffcddf-ad82-40d2-aaa0-c4f9c376ad65",
    #   "defaultCardIndicator" : false
    # }

    address_oid     = models.CharField(max_length=256, null=False)

    holder_name     = models.CharField(max_length=64, null=False)
    last_digits     = models.CharField(max_length=64, null=False)
    card_type       = models.CharField(max_length=64, null=False)
    payment_token   = models.CharField(max_length=64, null=False)

    default         = models.BooleanField(default=False, null=False,
                            help_text='whether this card is the default card to use')

    class Meta:
        abstract = False