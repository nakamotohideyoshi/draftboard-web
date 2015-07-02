#
# contest/forms.py

from django.forms import ModelForm, ModelChoiceField
from django.forms.widgets import SplitDateTimeWidget

from contest.models import Contest

class ContestForm(ModelForm):
    """
    The "create a contest" form which is backed by contest.models.Contest.

    This form is designed to hide some of the behind the scenes stuff,
    and help create a new contest as quickly and simply as possible.
    """

    clone_from = ModelChoiceField( Contest.objects.all(),
                        help_text="optional")

    class Meta:

        abstract = False

        #
        # ContestForm is backed by the model Contest
        model = Contest

        #
        # explicitly state the fields to display,
        # including any fields you will override with a widget
        fields = [
            'clone_from',
            'name',
            'prize_structure',
            'start',
            'end'
        ]

        #
        # add widgets, using the same field name from 'fields' list
        widgets = {
            'start' : SplitDateTimeWidget()
        }
