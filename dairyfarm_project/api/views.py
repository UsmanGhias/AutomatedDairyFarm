from django.shortcuts import render, redirect
from django.db.models import Sum
from rest_framework import viewsets
from .models import Farm, Cow
from .serializers import FarmSerializer, CowSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


#Farm Set View Model
class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']  # Allows partial updates

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

#Cow Set View Model
class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']  # Allows partial updates

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class MilkProductionReportView(APIView):
    def get(self, request):
        total_milk_production = Cow.objects.aggregate(Sum('milk_production'))
        return Response({'total_milk_production': total_milk_production})
#Cow Report View

def cow_report(request):
    cows = Cow.objects.all()
    return render(request, 'reports/cow_report.html', {'cows': cows})


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)