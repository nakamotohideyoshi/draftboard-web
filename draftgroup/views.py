#
# draftgroup/views.py

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.pagination import LimitOffsetPagination
from draftgroup.models import DraftGroup
from draftgroup.serializers import DraftGroupSerializer
from django.core.cache import caches

class DraftGroupAPIView(generics.GenericAPIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = DraftGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return DraftGroup.objects.get(pk=id)
        except DraftGroup.DoesNotExist:
            raise NotFound()

    def get(self, request, format=None):
        """
        given the GET param 'id', get the draft_group
        """
        pk = int(self.request.GET.get('id'))
        if pk is None or pk <= 0:
            raise ValidationError('GET param "id" not specified or is invalid: %s' % str(pk))
        #print( 'pk:', pk )
        c = caches['default']
        serialized_data = c.get(self.__class__.__name__ + str(pk), None)
        if serialized_data is None:
            serialized_data = DraftGroupSerializer( self.get_object(pk), many=False ).data
            c.add( self.__class__.__name__ + str(pk), serialized_data, 300 ) # 300 seconds
        return Response(serialized_data)

