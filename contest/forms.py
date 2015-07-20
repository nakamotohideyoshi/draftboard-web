#
# contest/forms.py

import django.forms as forms
from django.forms import ModelForm, ModelChoiceField, ValidationError
from django.forms.widgets import SplitDateTimeWidget
from contest.models import Contest
from util.midnight import midnight
from datetime import datetime

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
            'draft_group'           # not displayed by modeladmin however!
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

    ends_tonight = forms.BooleanField( initial=True,
        help_text='to set a custom time for the contest to end, you must set it below')

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
            'end',
            #'draft_group'
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
        # chekc it? if they picked it, i guess they want it

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
