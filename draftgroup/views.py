#
# draftgroup/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import LimitOffsetPagination
from draftgroup.models import DraftGroup
from draftgroup.serializers import DraftGroupSerializer

class DraftGroupAPIView(generics.ListAPIView):

    serializer_class = DraftGroupSerializer

    def get_queryset(self):
        """
        TODO - right now im getting all draft_groups,
                but we will want to accept arguments asap like contest_id
        """
        return DraftGroup.objects.all()