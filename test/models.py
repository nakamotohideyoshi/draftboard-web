
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from transaction.models import TransactionDetail, Balance
from sports.models import Game, PlayerStats, Player



#
# Test models must be created outside of the test
# class
class TransactionDetailChild(TransactionDetail):
    pass

class BalanceChild(Balance):
    pass


class GameChild(Game):
    class Meta:
        abstract = False

class PlayerChild(Player):
    class Meta:
        abstract = False

class PlayerStatsChild(PlayerStats):
    class Meta:
        abstract = False

# class Parent(models.Model):
#     """
#     quick test of generic foreign key for something else
#     """
#     created     = models.DateTimeField(auto_now_add=True, null=False)
#     val         = models.IntegerField(default=0, null=False)
#
#     #
#     # the generic foreign key to
#     parent_type = models.ForeignKey(ContentType)
#     parent_id   = models.PositiveIntegerField()
#     parent      = GenericForeignKey('parent_type', 'parent_id')
#
#     #grandchilds = GenericRelation('GrandChild', )
#
# class Child(models.Model):
#
#     created     = models.DateTimeField(auto_now_add=True, null=False)
#     text        = models.TextField(max_length=16, null=False, default='')
#
#     parents     = GenericRelation(Parent, content_type_field='parent_type',
#                                   object_id_field='parent_id')
#
#
#     class Meta:
#         abstract = True
#
# class GrandChild(Child):
#
#     text_2 = models.TextField(max_length=32, default='', null=False)
#
#     class Meta:
#         abstract = False