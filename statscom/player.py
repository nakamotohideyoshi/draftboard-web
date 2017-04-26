from logging import getLogger
logger = getLogger('statscom.player')


def get_fantasy_point_projection_from_stats_projection(stat_points, stats_projections, stat_map=None):
    """
    This takes a dict of stats_projections from stats.com fantasy projections and based upon our
    set of scoring.models.ScoreSystem scoring system it will calculate a fantasy point projection.

    Args:
        stat_points: Django Queryset: ScoreSystem.StatPoint
        stats_projections: dict of fantasy projections from stats.com api.
        stat_map: A dict that maps stats.com api fields to our internal scoring fields. (found
                    in statscom/constants.py)

    Returns: Float of projected fantasy points that will eventually be used to calculate a player's salary.
    """
    fp_total = 0

    if stat_map is None:
        raise Exception('stat_map missing from get_fantasy_point_projection_from_stats_projection()')

    if stats_projections is None:
        raise Exception('stats_projections missing from get_fantasy_point_projection_from_stats_projection()')

    if len(stat_points) < 1:
        raise Exception('stat_points missing from get_fantasy_point_projection_from_stats_projection()')

    logger.debug('========= get_fantasy_point_projection_from_stats_projection =============')
    for stat_point in stat_points:
        # For each stat in our stat map, try to find it in our player's projection list.
        if stat_point.stat in stat_map:
            # Does it exist in the projection? If so, add it to our total.
            if stat_map[stat_point.stat] in stats_projections.keys():
                stat_value = float(stats_projections[stat_map[stat_point.stat]]) * stat_point.value
                fp_total += stat_value
                logger.debug('%s %s is worth: %s' % (
                    stats_projections[stat_map[stat_point.stat]], stat_point.stat, stat_value ))
            else:
                logger.debug(
                    'projection for %s not found in this projection.' % stat_map[stat_point.stat])
        else:
            logger.warning('Player projection stat not found: %s' % stat_point.stat)

    logger.debug('Total projected FP: %s' % fp_total)
    return fp_total

