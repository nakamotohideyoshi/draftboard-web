#
# lobby/views.py

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from lobby.serializers import ContestBannerSerializer
from lobby.models import ContestBanner
from django.utils import timezone


class ContestBannerAPIView(generics.ListAPIView):
    """
    Get a list of the ContestBanner objects
    """
    serializer_class = ContestBannerSerializer

    def get_queryset(self):
        """
        return the QuerySet of the ContestBanner objects
        if the 'now' time is inbetween the start/end range
        and order the returned values by priority.
        """
        now = timezone.now()
        return ContestBanner.objects.filter(start_time__lte=now,
                                            end_time__gt=now).order_by('priority')

