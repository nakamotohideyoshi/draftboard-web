
from mysite.classes import  AbstractSiteUserClass
from .models import Tax
class TaxManager(AbstractSiteUserClass):
    def __init__(self, user):
        super().__init__(user)

    def info_collected(self):
        # TODO this needs to be stored elsewhere
        """

        :return: whether the information for taxes has been collected
        """
        try:
            Tax.objects.get(user=self.user)
        except Tax.DoesNotExist:
            return False
        return True


    def set_tax_id(self, tax_id):
        try:
            tax = Tax.objects.get(user=self.user)
        except Tax.DoesNotExist:
            tax  = Tax()
            tax.user = self.user
        tax.tax_identifier = tax_id
        tax.save()











