from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Forecasts, ForecastPoints, Resolutions
from .serializers import forecasts_serializer, forecast_points_serializer, resolutions_serializer

class ForecastsViewSet(viewsets.ModelViewSet):
    queryset = Forecasts.objects.all()
    serializer_class = forecasts_serializer

class ForecastPointsViewSet(viewsets.ModelViewSet):
    queryset = ForecastPoints.objects.all()
    serializer_class = forecast_points_serializer

class ResolutionsViewSet(viewsets.ModelViewSet):
    queryset = Resolutions.objects.all()
    serializer_class = resolutions_serializer

