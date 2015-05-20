from rest_framework import serializers
from .models import Ticket, TicketAmount
class TicketValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAmount
        fields = ("amount",)
class TicketSerializer(serializers.ModelSerializer):
    amount =TicketValueSerializer()

    class Meta:
        model = Ticket
        fields = ("pk","amount", "created")


