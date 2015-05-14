# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def load_initial_scoring_systems(apps, schema_editor):
    """
    load the initial scoring systems for the 4 major sports

    :param apps:
    :param schema_editor:
    :return:
    """

    sports = {
        'nba' : [
            ('point',       1.0),       # all points are worth 1.0 fantasy points
            ('three_pm',    0.5),       # three-point shot made
            ('rebound',     1.25),      # any rebound
            ('assist',      1.5),       # assists
            ('steal',       2.0),       # steals
            ('block',       2.0),       # blocked shot successful
            ('turnover',    -0.5),      # turnovers are worth negative points
            ('dbl-dbl',     1.5),       # two 10+ categories from (points, rebs, asts, blks, steals)
            ('triple-dbl',  3.0)        # three 10+ categories from (points, rebs, asts, blks, steals)
        ],
        'mlb' : [
            ('single',  3.0),           # hitter - singles
            ('double',  5.0),           # hitter - doubles
            ('triple',  8.0),           # hitter - triples
            ('hr',      10.0),          # hitter - home runs
            ('rbi',     2.0),           # hitter - runs batted in
            ('run',     2.0),           # hitter - runs scored
            ('bb',      2.0),           # hitter - walks
            ('hbp',     2.0),           # hitter - hit by pitch
            ('sb',      5.0),           # hitter - stolen bases
            ('cs',      -2.0),          # hitter - # times caught stealing
            # --
            ('ip',      2.25),          # pitcher - inning pitched
            ('k',       2.0),           # pitcher - strikeout
            ('win',     4.0),           # pitcher - Win
            ('er',      -2.0),          # pitcher - earned runs allowed
            ('hit',     -0.6),          # pitcher - hits against
            ('walk',    -0.6),          # pitcher - walked batters
            ('cg',      2.5),           # pitcher - complete game
            ('cgso',    2.5),           # pitcher - complete game AND shutout
            ('no-hitter', 5.0)          # pitcher - complete game AND no hits allowed
        ],
        'nhl' : [
            ('goal',    3.0),           # goals scored
            ('assist',  2.0),           # assists
            ('sog',     0.5),           # shots on goal
            ('blk',     0.5),           # blocked shot
            ('sh-bonus', 1.0),          # bonus points for goals/assists when shorthanded
            ('so-goal', 0.2),           # goal in a shootout
            ('hat',     1.5),           # hattrick is 3 goals scored
            # --
            ('win',     3.0),           # goalie - win
            ('save',    0.2),           # goalie - shots saved
            ('ga',      -1.0),          # goalie - goals allowed
            ('shutout', 2.0)            # goalie - complete game(includes OT) no goals (doesnt count shootout goals)
        ],
        'nfl' : [
            ('pass-td',     4.0),       # thrown touchdowns
            ('pass-yds',    0.04),      # pts per passing yard
            ('pass-bonus',  3.0),       # bonus for passing 300+ yards
            ('pass-int',    -1.0),      # passed interceptions
            # --
            ('rush-yds',    0.1),       # rushing points per yard
            ('rush-td',     6.0),       # rushed touchdowns
            ('rush-bonus',  3.0),       # bonus for rushing 100+ yards
            # --
            ('rec-yds',    0.1),        # receiving points per yard
            ('rec-td',     6.0),        # receiving touchdowns
            ('rec-bonus',  3.0),        # bonus for receiving 100+ yards

            ('ppr',        1.0),        # points per reception

            ('fumble-lost', -1.0),      # fumble lost (offensive player)
            ('two-pt-conv', 2.0),       # passed, rushed, or received succesful 2-pt conversion
            ('off-fum-td',  6.0),       # offensive fumble recovered for TD (unique situation)

            # -- dst scoring --
            ('sack',        1.0),       # sacks
            ('ints',        2.0),       # interceptions
            ('fum-rec',     2.0),       # fumble recoveries
            ('kick-ret-td', 6.0),       # kickoff returned for TD
            ('punt-ret-td', 6.0),       # punt returned for TD
            ('int-ret-td',  6.0),       # int returned for TD
            ('fum-ret-td',  6.0),       # fumble recovered for TD
            ('blk-punt-ret-td', 6.0),   # blocked punt returned for TD
            ('fg-ret-td',   6.0),       # missed FG, returned for TD
            ('safety',      2.0),       # safeties
            ('blk-kick',    2.0),       # blocked kick

            ('pa-0',        10.0),      # 0 points allowed
            ('pa-6',        7.0),       # 6 or less points allowed
            ('pa-13',       4.0),       # 13 or less points allowed
            ('pa-20',       1.0),       # 20 or less points allowed
            ('pa-27',       0.0),       # 27 or less points allowed
            ('pa-34',       -1.0),      # 34 or less points allowed
            ('pa-35plus',    -4.0)      # 35 or MORE points allowed
        ]
    }

    ScoreSystem = apps.get_model('scoring', 'ScoreSystem')
    StatPoint   = apps.get_model('scoring', 'StatPoint')

    for the_sport, stat_points_list in sports.items():
        ss = ScoreSystem()
        ss.sport        = the_sport
        ss.name         = 'salary'
        ss.description  = 'initial scoring system'
        ss.save()

        for stat_pt in stat_points_list:
            sp = StatPoint()
            sp.score_system = ss
            sp.stat         = stat_pt[0]    # string
            sp.value        = stat_pt[1]    # float
            sp.save()

class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScoreSystem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sport', models.CharField(max_length=64, default='')),
                ('name', models.CharField(max_length=64, default='')),
                ('description', models.CharField(max_length=1024, default='')),
            ],
        ),
        migrations.CreateModel(
            name='StatPoint',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('stat', models.CharField(max_length=32, default='')),
                ('value', models.FloatField(default=0.0)),
                ('str_format', models.CharField(max_length=32, default='')),
                ('score_system', models.ForeignKey(to='scoring.ScoreSystem')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='scoresystem',
            unique_together=set([('sport', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='statpoint',
            unique_together=set([('score_system', 'stat')]),
        ),

        #
        # inject the initial scoring metrics for the four major sports
        migrations.RunPython( load_initial_scoring_systems )
    ]
