#
# lineup/views.py

from django.core.cache import caches
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from lineup.serializers import LineupSerializer, PlayerSerializer, \
                                CreateLineupSerializer, EditLineupSerializer, \
                                LineupIdSerializer, LineupUsernamesSerializer
from lineup.models import Lineup, Player
from lineup.classes import LineupManager
from lineup.tasks import edit_lineup, edit_entry
from lineup.exceptions import CreateLineupExpiredDraftgroupException, InvalidLineupSizeException, \
                                LineupInvalidRosterSpotException, PlayerDoesNotExistInDraftGroupException
from draftgroup.models import DraftGroup
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

class CreateLineupAPIView(generics.CreateAPIView):
    """
    create a new lineup
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = CreateLineupSerializer

    def post(self, request, format=None):
        draft_group_id  = request.data.get('draft_group')
        players         = request.data.get('players', [])
        name            = request.data.get('name', '')

        # the draft_group_id has been validated by the serializer
        try:
            draft_group = DraftGroup.objects.get(pk=draft_group_id)
        except DraftGroup.DoesNotExist:
            return Response(
                'Draft group does not exist',
                status=status.HTTP_403_FORBIDDEN
            )

        #
        # use the lineup manager to create the lineup
        try:
            lm = LineupManager( request.user )
        except:
            return Response(
                'Invalid user',
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            lineup = lm.create_lineup( players, draft_group, name)
        except CreateLineupExpiredDraftgroupException:
            return Response(
                'You can no longer create lineups for this draft group',
                status=status.HTTP_403_FORBIDDEN
            )
        except InvalidLineupSizeException:
            return Response(
                'You have not drafted enough players.',
                status=status.HTTP_403_FORBIDDEN
            )
        except LineupInvalidRosterSpotException:
            return Response(
                'One or more of the players are invalid for the roster.',
                status=status.HTTP_403_FORBIDDEN
            )
        except PlayerDoesNotExistInDraftGroupException as e:
            return Response(
                str(e),
                status=status.HTTP_403_FORBIDDEN
            )
        except: # catch anything
            return Response(
                'Unknown error.',
                status=status.HTTP_403_FORBIDDEN
            )

        # on successful lineup creation:
        return Response('Lineup created.', status=status.HTTP_201_CREATED)

class LineupUserAPIView(APIView):
    """
    Get the usernames for lineups by providing a list of lineup ids.
        OR
    Get the lineups for a given contest by providing a valid contest_id and search string
        OR
    Get the lineups for a given contest by providing a valid contest_id

    The 'lineup_ids' parameter overrides the lookup by name. (ie: if all parameters
        are specified, we will return data for the specified lineup_ids list)

    POST params:

        (Required)
        contest_id      :  the contest id to search for lineups in

        (Use lineup_ids OR search_str)
        lineup_ids      : list of lineup ids, ie: [123, 432, 5234]
            ... OR ...
        search_str      : the search string for the lineup name (lineup names are based on username)
            ... OR ...
        nothing and it will default ot using just the contest_id

    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = LineupUsernamesSerializer

    def get_serialized_lineups(self, lineups=[]):
        data = []
        for l in lineups:
            data.append( LineupIdSerializer(l).data )
        return data

    def post(self, request, *args, **kwargs):
        """
        get the Lineup objects
        """
        args    = request.data

        # get the contest_id post param - it is required
        contest_id      = args.get('contest_id', None)

        # get the lineup_ids or the search_str
        lineup_ids      = args.get('lineup_ids', [])
        search_str      = args.get('search_str', None)


        # return Response({}, status=status.HTTP_200_OK)
        # return Response({}, status=status.HTTP_401_UNAUTHORIZED)




        if contest_id is None:
            msg = 'The POST param "contest_id" is required along with either: "lineup_ids", "search_str"'
            raise ValidationError(msg)

        lm = LineupManager( self.request.user )

        if lineup_ids:
            #
            # return the lineup usernames for the lineups with the ids, in the particular contest
            #return lm.get_for_contest_by_ids( contest_id, lineup_ids)
            lineups = lm.get_for_contest_by_ids( contest_id, lineup_ids)
            serialized_lineup_data = self.get_serialized_lineups(lineups)
            return Response( serialized_lineup_data, status=status.HTTP_200_OK)

        elif search_str:
            #
            # get the distinct lineups in this contest where the lineup_id matches
            #return lm.get_for_contest_by_search_str(contest_id, search_str)
            lineups = lm.get_for_contest_by_search_str(contest_id, search_str)
            serialized_lineup_data = self.get_serialized_lineups(lineups)
            return Response(serialized_lineup_data, status=status.HTTP_200_OK)
        else:
            lineups = lm.get_for_contest(contest_id)
            serialized_lineup_data = self.get_serialized_lineups(lineups)
            return Response(serialized_lineup_data, status=status.HTTP_200_OK)


class EditLineupAPIView(generics.CreateAPIView):
    """
    edit an existing lineup
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = EditLineupSerializer

    def post(self, request, format=None):
        #print( request.data )
        lineup_id   = request.data.get('lineup')
        players     = request.data.get('players', [])
        name        = request.data.get('name','')

        #
        # validate the parameters passed in here.

        #
        # call task
        task_result = edit_lineup.delay(request.user, players, lineup_id)

        return Response('lineup created')


class PlayersAPIView(generics.GenericAPIView):
    """
    get the lineup Players
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = PlayerSerializer

    def get_object(self, id):
        return Player.objects.filter(lineup__id=id)

    def get(self, request, pk, format=None):
        """
        get the lineup along with its players
        """
        serialized_data = PlayerSerializer( self.get_object(pk), many=True ).data
        return Response(serialized_data)


class AbstractLineupAPIView(generics.ListAPIView):
    """
    Abstract class.
    """
    lineup_model            = None

    permission_classes      = (IsAuthenticated,)
    serializer_class        = LineupSerializer

    def get_queryset(self):
        """

        """
        return [] # TODO


class UserUpcomingAPIView(AbstractLineupAPIView):
    """
    Get the User's upcoming lineups which are before the draft group start time
    """

    lineup_model = Lineup

    def get_queryset(self):
        """
        get the Lineup objects
        """
        return Lineup.objects.filter( user=self.request.user,
                                      draft_group__start__gt=timezone.now() )


class UserLiveAPIView(AbstractLineupAPIView):
    """
    Get the User's lineups that are after the draft group start time, and within 12 hours of the end time
    """

    lineup_model = Lineup

    def get_queryset(self):
        """
        retrieve the Lineup objects
        """
        offset_hours = 12
        now = timezone.now()
        dt = now - timedelta(hours=offset_hours)
        #print('now', str(now), 'dt', str(dt))
        return Lineup.objects.filter( user=self.request.user,
                                      draft_group__start__lte=now,
                                      draft_group__end__gt=dt )


class UserHistoryAPIView(AbstractLineupAPIView):
    """
    Get a User's lineups that are within 12 hours of the draft group's end datetime
    """

    lineup_model = Lineup

    def get_queryset(self):
        """
        retrieve the Lineup objects
        """
        offset_hours = 12
        now = timezone.now()
        dt = now - timedelta(hours=offset_hours)
        #print(str(dt))
        return Lineup.objects.filter( user=self.request.user,
                                      draft_group__end__lte=dt )
