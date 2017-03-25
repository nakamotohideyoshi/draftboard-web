#
# sports/game_status.py

class GameStatus(object):
    """
    for discrepencies with the values returned by this class, please refer
    to the source extended documentation found on the SportRadar website:

        https://developer.sportradar.us/

    this object is in charge of making sense of granular boxscore game statuses.

    given an MLB boxscore game status like 'odelay', the method get_primary_status()
    will return, in this case: 'inprogress'.
    """

    class InvalidSportException(Exception): pass

    class InvalidGranularStatus(Exception): pass

    class UnknownPrimaryStatusException(Exception): pass

    scheduled   = 'scheduled'       # game has not yet begun to happen
    inprogress  = 'inprogress'      # game is happening
    closed      = 'closed'          # game happened and stats are finalized

    primary_statuses = [
        scheduled,
        inprogress,
        closed
    ]

    # known sport possibilities
    nfl = 'nfl'
    mlb = 'mlb'
    nba = 'nba'
    nhl = 'nhl'

    # a dict with sport names that point to maps where the
    # sport-radar-game-status key is used to lookup the primary game status.
    sports = {

        mlb : {
            # ordered how they appear in the source documentation for easily comparing the two
            'scheduled'     : scheduled,
            'inprogress'    : inprogress,
            'complete'      : closed,
            'closed'        : closed,
            'wdelay'        : inprogress,
            'fdelay'        : inprogress,
            'odelay'        : inprogress,
            'canceled'      : closed,
            'unnecessary'   : closed,
            'postponed'     : closed,
            'suspended'     : closed,       # suspended and will be rescheduled [...], continuing where they left off.
            'maintenance'   : inprogress,   # failed review and is in the process of being repaired.
        },

        nfl : {
            # ordered how they appear in the source documentation for easily comparing the two
            'scheduled'     : scheduled,
            'inprogress'    : inprogress,
            'halftime'      : inprogress,
            'complete'      : closed,       # the game is over, but the statistics validation is not yet finished
            'closed'        : closed,       # game over, statistics validation done
            'canceled'      : closed,
            'postponed'     : closed,       # for dfs purposes, it closed because it wont happen on original date
            'delayed'       : inprogress,   # scheduled and inprogress games can enter this status
            'flex-schedule' : scheduled,    # scheduled with datetime, but likely to be moved for broadcast purposes
            'time-tbd'      : scheduled,    # scheduled to occur, date known, start time not yet determined
        },

        nba : {
            'scheduled'     : scheduled,
            'created'       : inprogress,   # the game just started, along with real-time data being available
            'inprogress'    : inprogress,
            'halftime'      : inprogress,
            'complete'      : closed,       # the game is over, but the statistics validation is not yet finished
            'closed'        : closed,       # game over, statistics validation done
            'canceled'      : closed,
            'delayed'       : inprogress,   # scheduled and inprogress games can enter this status
            'postponed'     : closed,       # for dfs purposes, it closed because it wont happen on original date
            'time-tbd'      : scheduled,    # scheduled to occur, date known, start time not yet determined
            'unnecessary'   : closed,       # a team won/clinched a series early, making this game unnecessary
        },

        # these statuses were taken from the classic feed on 2016.07.08,
        # we are assuming the official feed holds similar values
        # but its specific documentation is not out yet.
        nhl : {
            'scheduled'     : scheduled,
            'created'       : inprogress,   # the game just started, along with real-time data being available
            'inprogress'    : inprogress,
            'complete'      : closed,       # the game is over, but the statistics validation is not yet finished
            'closed'        : closed,       # game over, statistics validation done
            'canceled'      : closed,
            'delayed'       : inprogress,   # scheduled and inprogress games can enter this status
            'postponed'     : closed,       # for dfs purposes, it closed because it wont happen on original date
            'time-tbd'      : scheduled,    # scheduled to occur, date known, start time not yet determined
            'unnecessary'   : closed,       # a team won/clinched a series early, making this game unnecessary
        },
    }

    def __init__(self, sport):
        """
        :param sport: string name of the sport you want to use the GameStatus object for.
        :raise InvalidSportException: if the 'sport' arg not found among top-level keys in the status map
        """
        if sport not in self.sports.keys():
            err_msg = 'update sports.game_status.GameStatus for sport: %s' % sport
            #print(err_msg)
            raise self.InvalidSportException(err_msg)

        self.status_map = self.sports.get(sport)

    def get_primary_status(self, status):
        """
        given a granular boxscore status, return the overarching status
        in [scheduled, inprogress, closed].

        :param status: the granular (or specific) status. examples: 'odelay', 'time-tbd'
        :raise InvalidGranularStatus: the key for this granular status does not exist
        :raise UnknownPrimaryStatusException: if the granular status does not map to a primary status
        """
        # print('>>>', str(self.status_map))
        if status not in self.status_map.keys():
            err_msg = '%s does not exist and therefore cant have a primary status!' % status
            #print(err_msg)
            raise self.InvalidGranularStatus(err_msg)

        primary_status = self.status_map.get(status)
        if primary_status is None:
            err_msg = '%s does not map to a primary position. update sports.game_status.GameStatus asap' % status
            #print(err_msg)
            raise self.UnknownPrimaryStatusException(err_msg)

        return primary_status
