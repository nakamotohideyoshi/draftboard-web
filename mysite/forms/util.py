#
# mysite/forms/util.py

from django.forms import Form
from collections import OrderedDict

class OrderableFieldForm( Form ):
    """
    Works in django 1.8

    Example usage:

    """

    order = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.order = [
        #     'title',
        #     'question',
        #     'answer',
        #     'correct_answer',
        #     'incorrect_answer'
        # ]

        self.fields = self.reorder_fields(self.fields, self.order)

    def reorder_fields(self, fields, order):
        """
        If the self.key_order

        Reorder form fields by order, removing items not in order.

            Usage example for inheriting class:

            from django import forms
            class CustomForm( OrderableFieldForm ):

                order = [
                    'a_field',
                    'c_field',
                    'b_field'
                ]

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                #
                # the fields in your form...
                a_field = forms.IntegerField()
                b_field = forms.FloatField()
                c_field = forms.BooleanField()

        """
        if order is None:
            return fields

        else:
            for key, v in fields.items():
                if key not in order:
                    del fields[key]

            return OrderedDict(sorted(fields.items(), key=lambda k: order.index(k[0])))

