"""
This maps the stat projections we get from stats.com to our internal scoring fields that exist in
scoring.models.StatPoint. The value is what stats.com calls the field, the key is our internal field
value found in ScoreSystem.models.StatPoint (this is exposed in the admin panel)
"""
STATPOINT_TO_STATSCOM_NBA = {
    # points scored (fgs, foul shots, whatever)
    'point': 'points',
    # three-point shot made
    'three_pm': 'threePointMade',
    # any rebound
    'rebound': 'rebounds',
    # assists
    'assist': 'assists',
    # steals
    'steal': 'steals',
    # blocked shot successful
    'block': 'blocks',
    # turnovers are worth negative points
    'turnover': 'turnovers',
    # two 10+ categories from (points, rebs, asts, blks, steals)
    'dbl-dbl': 'doubleDoubles',
    # three 10+ categories from (points, rebs, asts, blks, steals)
    'triple-dbl': 'tripleDoubles',
}

STATPOINT_TO_STATSCOM_MLB = {
    # Pitcher
    'hit-batsman': 'hitBatsmen',
    'no-hitter': 'noHitters',
    'cgso': 'shutouts',
    'cg': 'completeGames',
    'walk': 'walks',
    'hit': 'hits',
    'er': 'earnedRuns',
    'win': 'wins',
    'k': 'strikeouts',
    'ip': 'inningsPitched',

    # Hitter
    'cs': 'caughtStealing',
    'sb': 'stolenBases',
    'hbp': 'hitByPitch',
    'bb': 'walks',
    'run': 'runs',
    'rbi': 'runsBattedIn',
    'hr': 'homeRuns',
    'triple': 'triples',
    'double': 'doubles',
    'single': 'singles',
}

STATPOINT_TO_STATSCOM_NFL = {
    # 'completions': '',
    # 'fieldGoalsMade': '',
    'pass-td': 'passTouchdowns',
    # 'extraPointsAttempted': '',
    'rec-td': 'receptionTouchdowns',
    'pass-yds': 'passYards',
    'ppr': 'receptions',
    # 'fieldGoalsMade29': '',
    # 'fieldGoalsMade49': '',
    # 'chance100RushYards': '',
    # 'fieldGoalsMade19': '',
    'fumble-lost': 'fumblesLost',
    'two-pt-conv': 'twoPointConversions',
    # 'fieldGoalsMade39': '',
    'pass-int': 'interceptions',
    # 'chance100ReceptionYards': '',
    # 'chance300PassYards': '',
    # 'extraPointsMade': '',
    # 'fieldGoalsAttempted': '',
    # 'fieldGoalsMade50': '',
    'rec-yds': 'receptionYards',
    # 'rushes': '',
    'rush-yds': 'rushYards',
    'rush-td': 'rushTouchdowns',
}
