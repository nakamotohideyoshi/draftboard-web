#
# draftgroup/views.py

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.pagination import LimitOffsetPagination
from draftgroup.models import DraftGroup
from draftgroup.classes import DraftGroupManager
from draftgroup.serializers import DraftGroupSerializer
from django.core.cache import caches

import json
from django.http import HttpResponse
from django.views.generic import View

class DraftGroupAPIView(generics.GenericAPIView):
    """
    return the draft group players for the given draftgroup id
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = DraftGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return DraftGroup.objects.get(pk=id)
        except DraftGroup.DoesNotExist:
            raise NotFound()

    def get(self, request, pk, format=None):
        """
        given the GET param 'id', get the draft_group
        """
        c = caches['default']
        serialized_data = c.get(self.__class__.__name__ + str(pk), None)
        if serialized_data is None:
            serialized_data = DraftGroupSerializer( self.get_object(pk), many=False ).data
            c.add( self.__class__.__name__ + str(pk), serialized_data, 300 ) # 300 seconds
        return Response(serialized_data)

class DraftGroupFantasyPointsView(View):
    """
    return all the lineups for a given contest as raw bytes, in our special compact format
    """

    def get(self, request, draft_group_id):
        dgm = DraftGroupManager()
        draft_group = dgm.get_draft_group( draft_group_id )
        data = {
            'draft_group'   : draft_group_id,
            'players'       : dgm.get_player_stats( draft_group=draft_group ),
        }
        #return HttpResponse( dgm.get_player_stats( draft_group=draft_group ) )
        return HttpResponse(json.dumps(data), content_type="application/json" )

