#
# sports/nfl/models.py

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
import sports.models
from django.db.models.signals import post_save

# Any classes that still have the abtract = True, just havent been migrated/implemented yet!

DST_PLAYER_LAST_NAME    = 'DST' # dst Player objects last_name
DST_POSITION            = 'DST' # dont change this

class Season( sports.models.Season ):
    class Meta:
        abstract = False

class Team( sports.models.Team ):
    """

    !!!!
    NOTE: there is a special signal hooked up to the post_save of
            this model. that signal creates the "dst player" that
            is related to this team. (we dont get DST's by default!)


    """

    # db.team.findOne({'parent_api__id':'hierarchy'})
    # {
    #     "_id" : "cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkNDM1MzEzOGQtNGMyMi00Mzk2LTk1ZDgtNWY1ODdkMmRmMjVjY29uZmVyZW5jZV9faWQzOTYwY2ZhYy03MzYxLTRiMzAtYmMyNS04ZDM5M2RlNmY2MmZkaXZpc2lvbl9faWQ1NGRjNzM0OC1jMWQyLTQwZDgtODhiMy1jNGMwMTM4ZTA4NWRpZDU4M2VjZWE2LWZiNDYtMTFlMS04MmNiLWY0Y2U0Njg0ZWE0Yw==",
    #     "alias" : "MIA",
    #     "id" : "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
    #     "market" : "Miami",
    #     "name" : "Heat",
    #     "parent_api__id" : "hierarchy",
    #     "dd_updated__id" : NumberLong("1431472829579"),
    #     "league__id" : "4353138d-4c22-4396-95d8-5f587d2df25c",
    #     "conference__id" : "3960cfac-7361-4b30-bc25-8d393de6f62f",
    #     "division__id" : "54dc7348-c1d2-40d8-88b3-c4c0138e085d",
    #     "venue" : "b67d5f09-28b2-5bc6-9097-af312007d2f4"
    # }

    srid_league   = models.CharField(max_length=64, null=False,
                            help_text='league sportsradar id')
    srid_conference   = models.CharField(max_length=64, null=False,
                            help_text='conference sportsradar id')
    srid_division   = models.CharField(max_length=64, null=False,
                            help_text='division sportsradar id')
    market      = models.CharField(max_length=64)

    class Meta:
        abstract = False

class Game( sports.models.Game ):
    """
    all we get from the inherited model is: 'start' and 'status'
    """
    home = models.ForeignKey( Team, null=False, related_name='game_hometeam')
    srid_home   = models.CharField(max_length=64, null=False,
                                help_text='home team sportsradar global id')

    away = models.ForeignKey( Team, null=False, related_name='game_awayteam')
    srid_away   = models.CharField(max_length=64, null=False,
                                help_text='away team sportsradar global id')
    title       = models.CharField(max_length=128, null=True)

    weather_json = models.CharField(max_length=512, null=False)

    class Meta:
        abstract = False

class GameBoxscore( sports.models.GameBoxscore ):
    clock       = models.CharField(max_length=16, null=False, default='')
    completed   = models.CharField(max_length=64, null=False, default='')
    quarter     = models.CharField(max_length=16, null=False, default='')

    class Meta:
        abstract = False

class Player( sports.models.Player ):
    """
    inherited: 'srid', 'first_name', 'last_name'
    """
    team        = models.ForeignKey(Team, null=False)
    srid_team = models.CharField(max_length=64, null=False, default='')
    birth_place = models.CharField(max_length=64, null=False, default='')
    birthdate   = models.CharField(max_length=64, null=False, default='')
    college     = models.CharField(max_length=64, null=False, default='')
    experience  = models.FloatField(default=0.0, null=False)
    height      = models.FloatField(default=0.0, null=False, help_text='inches')
    weight      = models.FloatField(default=0.0, null=False, help_text='lbs')
    jersey_number = models.CharField(max_length=64, null=False, default='')

    position = models.CharField(max_length=64, null=False, default='')
    primary_position = models.CharField(max_length=64, null=False, default='')

    status = models.CharField(max_length=64, null=False, default='',
                help_text='roster status - ie: "ACT" means they are ON the roster. Not particularly active as in not-injured!')

    draft_pick = models.CharField(max_length=64, null=False, default='')
    draft_round = models.CharField(max_length=64, null=False, default='')
    draft_year = models.CharField(max_length=64, null=False, default='')
    srid_draft_team = models.CharField(max_length=64, null=False, default='')

    class Meta:
        abstract = False

class PlayerStats( sports.models.PlayerStats ):

    # player  = models.ForeignKey(Player, null=False)
    # game    = models.ForeignKey(Game, null=False)

    # passing
    pass_td     = models.IntegerField(default=0, null=False)
    pass_yds    = models.IntegerField(default=0, null=False)
    pass_int    = models.IntegerField(default=0, null=False)

    # rushing
    rush_td     = models.IntegerField(default=0, null=False)
    rush_yds    = models.IntegerField(default=0, null=False)

    # receiving
    rec_td      = models.IntegerField(default=0, null=False)
    rec_yds     = models.IntegerField(default=0, null=False)
    rec_rec     = models.IntegerField(default=0, null=False)

    # (offensive) fumbles lost
    off_fum_lost = models.IntegerField(default=0, null=False)
    # (offensive) fum recovery for td
    off_fum_rec_td = models.IntegerField(default=0, null=False)

    # 2 point conversion
    two_pt_conv     = models.IntegerField(default=0, null=False)

    #
    # defensive stats:
    sack            = models.IntegerField(default=0, null=False)
    ints            = models.IntegerField(default=0, null=False)
    fum_rec         = models.IntegerField(default=0, null=False)

    # return tds
    ret_kick_td     = models.IntegerField(default=0, null=False)
    ret_punt_td     = models.IntegerField(default=0, null=False)
    ret_int_td      = models.IntegerField(default=0, null=False)
    ret_fum_td      = models.IntegerField(default=0, null=False)
    ret_blk_punt_td = models.IntegerField(default=0, null=False)
    ret_fg_td       = models.IntegerField(default=0, null=False)
    ret_blk_fg_td   = models.IntegerField(default=0, null=False)

    # misc
    sfty            = models.IntegerField(default=0, null=False)
    blk_kick        = models.IntegerField(default=0, null=False)

    # stats which factor into the DST "points allowed"
    #  ... includes safeties against the teams offense,
    #      plus interceptions and fumbles returned for TDs!
    int_td_against  = models.IntegerField(default=0, null=False)
    fum_td_against  = models.IntegerField(default=0, null=False)
    off_pass_sfty   = models.IntegerField(default=0, null=False)
    off_rush_sfty   = models.IntegerField(default=0, null=False)
    off_punt_sfty   = models.IntegerField(default=0, null=False)

    class Meta:
        abstract = False

class PlayerStatsSeason( sports.models.PlayerStatsSeason ):
    class Meta:
        abstract = True # TODO

class Injury( sports.models.Injury ):
    class Meta:
        abstract = True # TODO

class RosterPlayer( sports.models.RosterPlayer ):
    class Meta:
        abstract = True # TODO

class Venue( sports.models.Venue ):
    class Meta:
        abstract = True # TODO

class GamePortion(sports.models.GamePortion):
    class Meta:
        abstract = False

class PbpDescription(sports.models.PbpDescription):
    class Meta:
        abstract = False

class Pbp(sports.models.Pbp):
    class Meta:
        abstract = False

def create_dst_player(sender, **kwargs):
    """
 signal handler to create the DST Player object after a Team object is created.
    """
    if 'created' in kwargs:
        if kwargs['created']:
            instance = kwargs['instance']
            # ctype = ContentType.objects.get_for_model(instance)
            # entry = Player.objects.get_or_create(content_type=ctype,
            #                                         object_id=instance.id,
            #                                         pub_date=instance.pub_date)
            print( 'DEBUG: hi im the signal --', type(instance) )
            dst = Player()
            dst.team        = instance
            dst.srid        = instance.srid     #
            dst.first_name  = instance.name     # ie: "Patriots"
            dst.last_name   = DST_PLAYER_LAST_NAME
            dst.position    = DST_POSITION
            dst.primary_position = DST_POSITION
            dst.status      = ''
            dst.save() # commit changes

post_save.connect(create_dst_player, sender=Team)