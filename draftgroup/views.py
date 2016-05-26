#
# draftgroup/views.py

from dataden.classes import DataDen
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.pagination import LimitOffsetPagination
from draftgroup.models import DraftGroup, UpcomingDraftGroup, CurrentDraftGroup
from draftgroup.classes import DraftGroupManager
from draftgroup.serializers import (
    DraftGroupSerializer,
    UpcomingDraftGroupSerializer,
)
from django.core.cache import caches
from sports.classes import SiteSportManager
import json
from django.http import HttpResponse
from django.views.generic import View


class DraftGroupAPIView(generics.GenericAPIView):
    """
    return the draft group players for the given draftgroup id
    """

    DEFAULT_CACHE_TIMEOUT = 5 * 60 # 48 * 24 * 60 * 60

    serializer_class = DraftGroupSerializer

    def get_object(self, id):
        try:
            return DraftGroup.objects.get(pk=id)
        except DraftGroup.DoesNotExist:
            raise NotFound()

    def get_cache_key(self, pk):
        return self.__class__.__name__ + str(pk)

    def get(self, request, pk, format=None):
        """
        given the GET param 'id', get the draft_group
        """
        draft_group = self.get_object(pk)
        c = caches['default']
        serialized_data = c.get(self.get_cache_key(pk), None)
        if serialized_data is None or (draft_group.closed is not None and serialized_data.get('closed', None) is None):
            serialized_data = DraftGroupSerializer( self.get_object(pk), many=False ).data
            c.add( self.get_cache_key(pk), serialized_data, self.DEFAULT_CACHE_TIMEOUT )

        # # skip cache for testing
        # draft_group = self.get_object(pk)
        # serialized_data = DraftGroupSerializer( self.get_object(pk), many=False ).data
        return Response(serialized_data)


class UpcomingDraftGroupAPIView(generics.ListAPIView):
    """
    return the draft group players for the given draftgroup id
    """

    serializer_class        = UpcomingDraftGroupSerializer

    def get_queryset(self):
        """
        Return a QuerySet from the UpcomingDraftGroup model (DraftGroup objects).
        """
        return UpcomingDraftGroup.objects.all()

class CurrentDraftGroupAPIView(generics.ListAPIView):
    """
    return the draft group players for the given draftgroup id
    """

    # Current and Upcoming use the same serializer
    serializer_class        = UpcomingDraftGroupSerializer

    def get_queryset(self):
        """
        Return a QuerySet from the UpcomingDraftGroup model (DraftGroup objects).
        """
        return CurrentDraftGroup.objects.all()

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


class DraftGroupGameBoxscoresView(View):
    """
    return all the boxscores for the given draft group (basically, all
    the live games (ie: Home @ Away with scores) from the context
    of the draftgroup)
    """

    def __add_to_dict(self, target, extras):
        for k,v in extras.items():
            target[ k ] = v
        return target

    def get(self, request, draft_group_id):

        dgm = DraftGroupManager()
        try:
            draft_group = dgm.get_draft_group( draft_group_id )
        except DraftGroup.DoesNotExist:
            return HttpResponse( {}, content_type='application/json', status=status.HTTP_404_NOT_FOUND)

        site_sport  = draft_group.salary_pool.site_sport
        ssm         = SiteSportManager()
        games       = dgm.get_games( draft_group )
        game_serializer_class = ssm.get_game_serializer_class(site_sport)

        boxscores   = dgm.get_game_boxscores( draft_group )
        boxscore_serializer_class = ssm.get_boxscore_serializer_class(site_sport)

        # data = []
        # for b in boxscores:
        #     data.append( b.to_json() )
        data = {}
        for game in games:
            # initial inner_data
            inner_data = {}

            # add the game data
            g = game_serializer_class( game ).data
            self.__add_to_dict( inner_data, g )

            # add the boxscore data
            boxscore = None
            try:
                boxscore = boxscores.get(srid_game=game.srid) # may not exist
            except:
                pass
            b = {}
            if boxscore is not None:
                b = {
                    'boxscore' : boxscore_serializer_class( boxscore ).data
                }
            self.__add_to_dict( inner_data, b )

            # finish it by adding the game data to the return data dict
            data[ game.srid ] = inner_data

        return HttpResponse( json.dumps(data), content_type='application/json' )


class DraftGroupPbpDescriptionView(View):
    """
    return the most recent PbpDescription objects for this draft group
    """

    def get(self, request, draft_group_id):

        dgm = DraftGroupManager()
        draft_group = dgm.get_draft_group( draft_group_id )
        boxscores = dgm.get_game_boxscores( draft_group )

        dd = DataDen()
        game_srids = []
        for b in boxscores:
            game_srids.append( b.srid_game )

        game_events = dd.find('nba','event','pbp', {'game__id':{'$in':game_srids}})
        events = []
        for e in game_events:
            events.append( e )

        return HttpResponse( json.dumps(events), content_type='application/json' )
