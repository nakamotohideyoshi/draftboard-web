#
# contest/forms.py

import django.forms as forms
from django.forms import ModelForm, ModelChoiceField, ValidationError
from django.forms.widgets import SplitDateTimeWidget
from contest.models import Contest
from util.midnight import midnight
from datetime import datetime
import draftgroup.classes
import draftgroup.exceptions
import mysite.exceptions

class ContestForm(ModelForm):
    """
    The "create a contest" form which is backed by contest.models.Contest.

    This form is designed to hide some of the behind the scenes stuff,
    and help create a new contest as quickly and simply as possible.
    """

    # clone_from = ModelChoiceField( Contest.objects.all(),
    #                   help_text="optional")

    # ends_tonight = forms.BooleanField( initial=True,
    #     help_text='to set a custom time for the contest to end, you must set it below')

    class Meta:

        abstract = False

        #
        # ContestForm is backed by the model Contest
        model = Contest

        #
        # explicitly state the fields to display,
        # including any fields you will override with a widget
        fields = [
            #'clone_from',
            'site_sport',
            'name',
            'prize_structure',
            'start',
            #'ends_tonight',         # make visible in modeladmin !
            'end',
            'draft_group',           # not displayed by modeladmin however!
            'max_entries',
            #'entries',
            'gpp',
            'respawn',
            'doubleup'
        ]

        # exclude = ('ends_tonight',)
        #
        # add widgets, using the same field name from 'fields' list
        # widgets = {
        #     'start' : SplitDateTimeWidget() # this widget is worse than the default one
        # }

    def clean(self):
        """
        custom form validation

        :return:
        """

        cleaned_data    = super().clean()

        site_sport      = cleaned_data.get('site_sport')
        if not site_sport:
            raise ValidationError( 'Select the sport for this Contest.' )

        name            = cleaned_data.get('name')
        if not name:
            raise ValidationError( 'Dude, you have to at least NAME the Contest.' )

        prize_structure = cleaned_data.get("prize_structure")
        # chekc it? if they picked it, i guess they want it

        start           = cleaned_data.get('start')
        if not start:
            raise ValidationError( 'If you dont choose a "start" time for the Contest, will it ever run? ... No.' )

        end             = cleaned_data.get('end', None)
        #ends_tonight    = cleaned_data.get('ends_tonight')

        # if ends_tonight and end:
        #     raise ValidationError( 'You cant set "Ends Tonight" and have a time set in "Custom End Time"')

        # # now we can dynamically create end based on 'ends_tonight' setting
        # if ends_tonight == True:
        #     # as long as there isnt a time set in 'end' we can dynamically create it for midnight
        #     end = midnight( start )
        #     self.cleaned_data['end'] = end

        # if end < start:
        #     raise ValidationError( 'The "end" time cant be before the "start" time... Do you know how time works!?')
        return cleaned_data

class ContestFormAdd(ContestForm):
    """
    The "create a contest" form which is backed by contest.models.Contest.

    This form is designed to hide some of the behind the scenes stuff,
    and help create a new contest as quickly and simply as possible.
    """

    # clone_from = ModelChoiceField( Contest.objects.all(),
    #                   help_text="optional")

    ends_tonight = forms.BooleanField( initial=True, required=False,
        help_text='to set a custom time for the contest to end, you must set it below')

    early_registration = forms.BooleanField( initial=False, required=False,
        help_text='do not let users draft teams for this contest yet, but allow them to buy in to reserve a spot.')

    class Meta:

        abstract = False

        #
        # ContestForm is backed by the model Contest
        model = Contest

        #
        # explicitly state the fields to display,
        # including any fields you will override with a widget
        fields = [
            #'clone_from',
            'site_sport',
            'name',
            'prize_structure',
            'start',
            'ends_tonight',
            'early_registration',
            'end',
            'draft_group',
            'max_entries',
            # 'entries',
            'gpp',
            'respawn',
            'doubleup'
        ]

        #
        # add widgets, using the same field name from 'fields' list
        # widgets = {
        #     'start' : SplitDateTimeWidget() # this widget is worse than the default one
        # }

    def clean(self):
        """
        custom form validation

        :return:
        """

        cleaned_data    = super().clean()

        site_sport      = cleaned_data.get('site_sport')
        if not site_sport:
            raise ValidationError( 'Select the sport for this Contest.' )

        name            = cleaned_data.get('name')
        if not name:
            raise ValidationError( 'Dude, you have to at least NAME the Contest.' )

        prize_structure = cleaned_data.get("prize_structure")


        start           = cleaned_data.get('start')
        if not start:
            raise ValidationError( 'If you dont choose a "start" time for the Contest, will it ever run? ... No.' )

        end             = cleaned_data.get('end', None)
        ends_tonight    = cleaned_data.get('ends_tonight')

        if ends_tonight and end:
            raise ValidationError( 'You cant set "Ends Tonight" and have a time set in "Custom End Time"')

        # now we can dynamically create end based on 'ends_tonight' setting
        if ends_tonight == True:
            # as long as there isnt a time set in 'end' we can dynamically create it for midnight
            end = midnight( start )
            print( 'end', str(end) )
            self.cleaned_data['end'] = end
        else:
            print('ends_tonight is False')

        if end < start:
            raise ValidationError( 'The "end" time cant be before the "start" time... Do you know how time works!?')

        #
        # typically early_registration will be false, and
        # we should automatically associate with the active draft group
        draft_group        = cleaned_data.get('draft_group', None)
        early_registration = cleaned_data.get('early_registration')
        if early_registration and draft_group is not None:
            raise ValidationError('You cant enable "early_registration" AND set a Draft Group.')
        elif early_registration == True:
            pass # dont set a draftgroup, let it be None
        elif draft_group is not None:
            pass # the draft_group they set will potentially be used after some validity checking
            # TODO -- should we do checking???
        else:
            #
            # get the active draftgroup for this contest
            dgm = draftgroup.classes.DraftGroupManager()
            try:
                draft_group = dgm.get_for_site_sport( site_sport, start, end )

            except draftgroup.exceptions.NotEnoughGamesException:
                raise ValidationError('There are not enough upcoming games for the '
                                      'sport in the range you specified.')
            except draftgroup.exceptions.NoGamesAtStartTimeException:
                raise ValidationError('There is no upcoming game for this sport'
                                      ' which matches the start time you chose. Please '
                                      'make sure the contest starts when a game starts.')
            except draftgroup.exceptions.EmptySalaryPoolException:
                raise ValidationError('A salary pool does not exist - so we can not '
                                      'create the draft group players. '
                                      'This error indicates that either: 1) base stats '
                                      'for the sport have not been set up yet or 2) '
                                      'a salary pool for the sport has not yet been created.')
            except mysite.exceptions.NoGamesInRangeException:
                raise ValidationError('Could not create Contest because there were '
                                      'no upcoming games in the date range specified.')

            self.cleaned_data['draft_group'] = draft_group

# class TemplateContestForm(ContestForm):
#     pass # TODO TODO TODO
#
# class TemplateContestFormAdd(ContestFormAdd):
#
#     class Meta:
#         abstract    = False
#         model       = Contest
#
#         #
#         # explicitly state the fields to display,
#         # including any fields you will override with a widget
#         fields = [
#             'site_sport',
#             'name',
#             'prize_structure',
#             'max_entries',
#             'entries',
#             'gpp',
#             'respawn',
#             'doubleup'
#         ]
#
#     # use the fields which we are explicity stating in the Meta class
#     fieldsets = (
#         # step 1: create the contest you want to add to the schedule
#         ('Step 1: Edit the Contest Template', {
#             'fields': (
#                 'site_sport',
#                 'name',
#
#                 'prize_structure',
#                 'max_entries',
#                 'entries',
#
#                 'gpp',
#                 'respawn',
#                 'doubleup'
#             )
#         }),
#
#         # step 2: choose the start time, and set a duration (hours) for the contest to run
#         ('Step 2: Choose a Start time, and Duration (hours).', {
#             'fields': (
#                 'start_time',       # a Time object, not a DateTime object
#                 'duration_minutes', # the end_time will, therefore be: (start_time + timedelta(minutes=duration_minutes))
#             )
#         }),
#
#         # step 3: select the days of the week you would like this contest to run
#         ('Step 3: Schedule this Contest for the selected days.', {
#             'fields': (
#                 'monday',
#                 'tuesday',
#                 'wednesday',
#                 'thursday',
#                 'friday',
#                 'saturday',
#                 'sunday'
#             )
#         })
#     )