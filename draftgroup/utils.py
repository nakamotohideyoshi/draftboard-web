from logging import getLogger

from django.contrib.contenttypes.models import ContentType

from draftgroup.models import Player as DraftgroupPlayer
from salary.models import Salary

logger = getLogger('draftgroup.utils')


def get_draftgroup_player_from_sport_player(sport_player, draft_group):
    """
    When editing a lineup, all we have is a <sport>.models.player and a draft group, but we
    need to get the draftgroup.models.player in order to update the lineup, There isn't a great
    way to do that so this function will get it for you.

    :param sport_player:
    :param draft_group:
    :return:
    """
    player_type = ContentType.objects.get_for_model(sport_player)

    salary_player = Salary.objects.get(
        player_type=player_type,
        player_id=sport_player.id,
        draft_group_player__draft_group=draft_group)

    logger.debug('Finding draftgroup.models.player for salary.models.player: %s' % salary_player)

    return DraftgroupPlayer.objects.get(salary_player=salary_player, draft_group=draft_group)
