#
# contest/schedule/forms.py

#
# contest/forms.py

from django.utils import timezone
import django.forms as forms
from django.forms import ModelForm, ModelChoiceField, ValidationError
from django.forms.widgets import SplitDateTimeWidget
#from django.forms.extras.widgets import xxx
#from contest.models import Contest
from contest.forms import ContestForm
from util.midnight import midnight
from datetime import datetime
import draftgroup.classes
from contest.schedule.models import TemplateContest, ScheduledTemplateContest

class TemplateContestForm(ContestForm):

    class Meta:
        abstract    = False
        model       = TemplateContest

        #
        # explicitly state the fields to display,
        # including any fields you will override with a widget
        fields = [
            'site_sport',
            'name',
            'prize_structure',
            'max_entries',
            'entries',
            'gpp',
            'respawn',
            'doubleup',

            #
            # some fields like 'start' are ignored
            # in the TemplateContest because they will
            # be scheduled by ScheduledTemplateContest
        ]

class TemplateContestFormAdd(TemplateContestForm):

    # start, end exist to override and set default values
    start   = forms.DateTimeField(initial=timezone.now())
    end     = forms.DateTimeField(initial=timezone.now())

    class Meta:
        abstract    = False
        model       = TemplateContest

        #
        # explicitly state the fields to display,
        # including any fields you will override with a widget
        fields = [
            'site_sport',
            'name',
            'prize_structure',
            'max_entries',
            'entries',
            'gpp',
            'respawn',
            'doubleup',

            'start',        # include it, so we can exclude it... really.
            'end',          # include it, so we can exclude it... really.
        ]

class ScheduledTemplateContestForm(ModelForm):

    class Meta:
        abstract    = False
        model       = ScheduledTemplateContest

        #
        # explicitly state the fields to display,
        # including any fields you will override with a widget
        fields = [
            'schedule',
            'template_contest',
            'start_time',
            'duration_minutes',
        ]
