from django.shortcuts import render
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Farm, Cow
from .serializers import FarmSerializer, CowSerializer
from api.models import Vendor, MilkCategory, vendorledger, Profile, CustomerMilkCategory, CustomerLedger
from .serializers import MilkCategorySerializer, VendorLedgerSerializer, ProfileSerializer, CustomerMilkCategorySerializer, CustomerLedgerSerializer
from django.shortcuts import render, redirect
from .models import Vendor, MilkCategory, Customer, Ledger
from .forms import VendorForm, MilkCategoryForm, CustomerForm, LedgerForm


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User


# Farm Set View Model
class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']  # Allows partial updates

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


# Cow Set View Model
class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']  # Allows partial updates

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class MilkCategoryViewSet(viewsets.ModelViewSet):
    queryset = MilkCategory.objects.all()
    serializer_class = MilkCategorySerializer

class VendorLedgerViewSet(viewsets.ModelViewSet):
    queryset = vendorledger.objects.all()
    serializer_class = VendorLedgerSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class CustomerMilkCategoryViewSet(viewsets.ModelViewSet):
    queryset = CustomerMilkCategory.objects.all()
    serializer_class = CustomerMilkCategorySerializer

class CustomerLedgerViewSet(viewsets.ModelViewSet):
    queryset = CustomerLedger.objects.all()
    serializer_class = CustomerLedgerSerializer




class MilkProductionReportView(APIView):
    def get(self, request):
        total_milk_production = Cow.objects.aggregate(Sum('milk_production'))
        return Response({'total_milk_production': total_milk_production})


# Cow Report View
def cow_report(request):
    cows = Cow.objects.all()
    return render(request, 'reports/cow_report.html', {'cows': cows})


# Register View
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        # Add your signup logic here
        pass
    else:
        # Add your signup form rendering logic here
        pass


# Vendor Views

def addvendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allvendor')
    else:
        form = VendorForm()
    
    return render(request, 'addvendor.html', {'form': form})


def add_milk_category(request):
    if request.method == 'POST':
        form = MilkCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allvendor')
    else:
        form = MilkCategoryForm()
    
    return render(request, 'add_milk_category.html', {'form': form})


def allvendor(request):
    vendors = Vendor.objects.all()
    return render(request, 'allvendor.html', {'vendors': vendors})


def ledger(request, pk):
    vendor = Vendor.objects.get(pk=pk)
    ledgers = Ledger.objects.filter(vendor=vendor)
    return render(request, 'ledger.html', {'vendor': vendor, 'ledgers': ledgers})


def ledger_save(request):
    if request.method == 'POST':
        form = LedgerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allvendor')
    else:
        form = LedgerForm()
    
    return render(request, 'ledger_save.html', {'form': form})


def ledger_delete(request):
    if request.method == 'POST':
        ledger_id = request.POST.get('ledger_id')
        ledger = Ledger.objects.get(pk=ledger_id)
        ledger.delete()
        return redirect('allvendor')


# Add Customer View

def addcustomer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allcustomer')
    else:
        form = CustomerForm()
    
    return render(request, 'addcustomer.html', {'form': form})


def customer_milk_category(request):
    if request.method == 'POST':
        form = MilkCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allcustomer')
    else:
        form = MilkCategoryForm()
    
    return render(request, 'customer_milk_category.html', {'form': form})


def customer_page(request):
    customers = Customer.objects.all()
    return render(request, 'customer_page.html', {'customers': customers})


def customer_ledger(request, pk):
    customer = Customer.objects.get(pk=pk)
    ledgers = Ledger.objects.filter(customer=customer)
    return render(request, 'customer_ledger.html', {'customer': customer, 'ledgers': ledgers})


def customer_ledger_save(request):
    if request.method == 'POST':
        form = LedgerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allcustomer')
    else:
        form = LedgerForm()
    
    return render(request, 'customer_ledger_save.html', {'form': form})


def customer_ledger_delete(request):
    if request.method == 'POST':
        ledger_id = request.POST.get('ledger_id')
        ledger = Ledger.objects.get(pk=ledger_id)
        ledger.delete()
        return redirect('allcustomer')


def allcustomer(request):
    customers = Customer.objects.all()
    return render(request, 'allcustomer.html', {'customers': customers})

