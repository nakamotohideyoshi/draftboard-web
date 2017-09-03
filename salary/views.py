from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from salary.classes import SalaryPool2Csv
from sports.models import SiteSport
from .models import SalaryConfig
from .serializers import (
    SalaryConfigSerializer,
    SalaryPlayer2CsvSerializer,
)


class PoolGeneratorView(View):
    template_name = 'pool_generator.html'

    def get(self, request, *args, **kwargs):
        sports = SiteSport.objects.all()
        confs = SalaryConfig.objects.all()
        return render(request, self.template_name, {'sports': sports, 'confs': confs})


class ConfigAPIView(generics.ListCreateAPIView):
    """
    Retrieves all SalaryConfig db data with all the TrailingGameWeight objects that
    point to it.
        * |api-text| :dfs:`salary/config/`
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = SalaryConfigSerializer
    queryset = SalaryConfig.objects.all()


class ConfigRetrieveAPIView(generics.RetrieveAPIView):
    """
    Retrieves a specific SalaryConfig based off the pk with all of the TrailingGameWeight objects
    that point to it.

        * |api-text| :dfs:`salary/config/retrieve/`
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = SalaryConfigSerializer
    lookup_field = "pk"
    queryset = SalaryConfig.objects.all()


class SalaryPlayers2CsvAPIView(APIView):
    """
    exports a csv file with the player salaries and player information
    for a specific salary pool.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SalaryPlayer2CsvSerializer

    @staticmethod
    def get(request, salary_pool_id, format=None):
        """
        Given the 'task' parameter, return the status of the task (ie: from performing the edit-entry)

        :param request:
        :param salary_pool_id:
        :param format:
        :return:
        :return:
        """
        # pseudo_buffer = self.Echo()
        # writer = csv.writer(pseudo_buffer)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="salaries.csv"'

        salary_pool_2_csv = SalaryPool2Csv(salary_pool_id, httpresponse=response)
        salary_pool_2_csv.generate()

        return response
