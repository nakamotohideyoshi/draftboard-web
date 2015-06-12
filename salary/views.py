from django.shortcuts import render
from django.views.generic import TemplateView, View
from sports.models import SiteSport
from .models import SalaryConfig, TrailingGameWeight, Pool
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import TrailingGameWeightSerializer, SalaryConfigSerializer
class PoolGeneratorView(View):
    template_name   = 'pool_generator.html'


    def get(self, request, *args, **kwargs):
        sports = SiteSport.objects.all()
        confs = SalaryConfig.objects.all()
        return render(request, self.template_name, {'sports':sports, 'confs':confs})


class ConfigAPIView( generics.ListCreateAPIView):
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

