#
# schedule/views.py

from django.views.generic.edit import CreateView, UpdateView
from contest.schedule.models import TemplateContest, ScheduledTemplateContest
from contest.schedule.forms import TemplateContestForm, TemplateContestFormAdd


# test the generic add view
class TemplateContestCreate(CreateView):
    model       = TemplateContest
    form_class  = TemplateContestFormAdd
    #fields      = ['name','ends_tonight','start']


# testing the generic edit view
class TemplateContestUpdate(UpdateView):
    model       = TemplateContest
    form_class  = TemplateContestForm
    #fields      = ['name','start']