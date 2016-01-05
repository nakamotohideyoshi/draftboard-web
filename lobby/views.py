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


class ContestBannerAPIView(generics.ListAPIView):
    """
    Get a list of the ContestBanner objects
    """
    serializer_class = ContestBannerSerializer

    def get_queryset(self):
        """
        return the QuerySet of the ContestBanner objects to return
        """
        return ContestBanner.objects.all()  # TODO - for now return all, we'll want more stuff
