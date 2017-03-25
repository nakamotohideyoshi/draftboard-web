"""
This Maps the stat projections we get from stats.com to our internal scoring fields that exist in
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

# TODO (zach) Once stats.com has projections, fill out this map to match them up.
STATPOINT_TO_STATSCOM_MLB = {
    'hit-batsman': '',
    'no-hitter': '',
    'cgso': '',
    'cg': '',
    'walk': '',
    'hit': '',
    'er': '',
    'win': '',
    'k': '',
    'ip': '',
    'cs': '',
    'sb': '',
    'hbp': '',
    'bb': '',
    'run': '',
    'rbi': '',
    'hr': '',
    'triple': '',
    'double': '',
    'single': '',
}
