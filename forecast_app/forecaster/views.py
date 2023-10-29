from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def forecast(request):
    return HttpResponse('This is the forecast page.')

def all_forecasts(request):
    return HttpResponse('This is the overview page')