# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def update_scoring_systems(apps, schema_editor):
    """
    update scoring systems for the 4 major sports

    :param apps:
    :param schema_editor:
    :return:
    """

    sports = {
        # dan: 2016-06-01 @ 1:11 PM
        # Hitters
        # Draftboard
        # Single
        # 2
        # Double
        # 4
        # Triple
        # 6
        # Home Run
        # 8
        # Walk / HBP
        # 2
        # Run
        # 1
        # RBI
        # 1
        # Steal
        # 1
        # Pitchers
        #
        #
        # Strikeout
        # 1
        # BB/H/HBP
        # -0.25
        # Earned Run
        # -1
        # Win
        # 2
        # IP
        # 1
        'mlb' : [
            ('sb',           1.0),          # lowered from 2.0 (migration 0002)
            ('hit-batsman', -0.25),         # new - pitcher hits a batter: -0.25, same as hits/walks
        ],
        'nhl' : [
            #
            # for NHL we added:
            ('blk_att',         0.5),           # new - blocked shots: 0.5pts
            ('ms',              0.5),           # new - missed shots : 0.5pts
        ],
        'nfl' : [
            # changes to player scoring:
            ('pass-bonus',      0.0),           # 100yd bonus: lowered from 3.0 (migration 0002)
            ('rush-bonus',      0.0),           # 100yd bonus: lowered from 3.0 (migration 0002)
            ('rec-bonus',       0.0),           # 100yd bonus: lowered from 3.0 (migration 0002)
            ('ppr',             0.5),           # lowered from 1.0 (migration 0002)

            ###### zero out DST scoring #####
            ('sack',            0.0),       # sacks
            ('ints',            0.0),       # interceptions
            ('fum-rec',         0.0),       # fumble recoveries

            ('int-ret-td',      0.0),       # int returned for TD
            ('fum-ret-td',      0.0),       # fumble recovered for TD
            ('blk-punt-ret-td', 0.0),       # blocked punt returned for TD
            ('fg-ret-td',       0.0),       # missed FG, returned for TD
            ('blk-fg-ret-td',   0.0),
            ('safety',          0.0),       # safeties
            ('blk-kick',        0.0),       # blocked kick

            ('pa-0',            0.0),       # 0 points allowed
            ('pa-6',            0.0),       # 6 or less points allowed
            ('pa-13',           0.0),       # 13 or less points allowed
            ('pa-20',           0.0),       # 20 or less points allowed
            ('pa-27',           0.0),       # 27 or less points allowed
            ('pa-34',           0.0),       # 34 or less points allowed
            ('pa-35plus',       0.0),       # 35 or MORE points allowed
        ],

        # NBA - no changes
    }

    ScoreSystem = apps.get_model('scoring', 'ScoreSystem')
    StatPoint   = apps.get_model('scoring', 'StatPoint')

    for the_sport, stat_points_list in sports.items():
        # nhl, nfl, nba, mlb ScoreSystems will exist
        ss = ScoreSystem.objects.get(sport=the_sport, name='salary')

        # just modify any values (or add new ones if they do not exist)
        for stat_name, stat_val in stat_points_list:
            try:
                sp = StatPoint.objects.get(score_system=ss, stat=stat_name)
            except StatPoint.DoesNotExist:
                sp = StatPoint()
                sp.score_system = ss
                sp.stat         = stat_name
            # now set the value and save (it will create or update it)
            sp.value = stat_val
            sp.save()

class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0002_auto_20150514_0112'),
    ]

    operations = [
        # update the scoring systems using the RunPython mechanism
        migrations.RunPython( update_scoring_systems )
    ]
