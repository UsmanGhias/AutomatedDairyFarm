from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Vendor, Profile
from .serializers import contactFormSerializer, SignUpFormSerializer, AddVendorFormSerializer, \
    MilkCategoryFormSerializer, VendorLedgerFormSerializer, ProfileFormSerializer, CustomerMilkCategoryFormSerializer

@api_view(['POST'])
def home(request):
    title = ''
    confirm_message = None
    serializer = contactFormSerializer(data=request.data)
    if serializer.is_valid():
        receivers_list = ['omarfaruk2468@gmail.com']
        subject = serializer.validated_data['subject']
        name = serializer.validated_data['name']
        comment = serializer.validated_data['message']
        email_from = serializer.validated_data['email']
        message = f'Name: {name}\nEmail Id: {email_from}\nMessage: {comment}'
        email_sender = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_sender, receivers_list, fail_silently=False)
        title = "Thanks! " + name
        confirm_message = "Thanks for the message. We will get right back to you."
    response_data = {'title': title, 'confirm_message': confirm_message}
    return Response(response_data)


@api_view(['POST'])
def signup(request):
    serializer = SignUpFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#*******************************************#
#       ||  Vendors Views Started  ||       #
#*******************************************#

# Add Vendor
@api_view(['GET', 'POST'])
def addvendor(request):
    vl = Vendor.objects.only('vendorname')
    if request.method == 'POST':
        serializer = AddVendorFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        serializer = AddVendorFormSerializer()
    return Response(serializer.data)


# Vendor MilkCategory
@api_view(['GET', 'POST'])
def add_milk_category(request):
    vl = Vendor.objects.only('vendorname')
    if request.method == 'POST':
        serializer = MilkCategoryFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        serializer = MilkCategoryFormSerializer()
    return Response(serializer.data)


# All vendors dashboard
@api_view(['GET'])
def allvendor(request):
    manager = ''
    if request.user.is_authenticated:
        manager = request.user.username
        vendor = Vendor.objects.filter(managername=manager)
        serializer = VendorSerializer(vendor, many=True)
        return Response(serializer.data)


# Individual vendor dashboard
@api_view(['GET'])
def ledger(request, pk):
    ledgerform = vendorledgerForm()
    vendor_obj = get_object_or_404(Vendor, pk=pk)
    ledgerdata = vendorledger.objects.filter(related_vendor=vendor_obj)
    alltotal = 0.0
    for alto in ledgerdata:
        alltotal = alltotal + float(alto.total)
    print(alltotal)

    milks = MilkCategory.objects.filter(related_vendor=vendor_obj)

    milk_list = [(milk.animalname + "-" + str(milk.milkprice), milk.pk) for milk in milks]
    print(milk_list)

    day_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return Response({
        "vendor_obj": vendor_obj,
        "ledgerdata": ledgerdata,
        "ledgerform": ledgerform,
        "num_range": range(6),
        "milk_list": milk_list,
        "day_list": day_list,
        "alltotal": alltotal,
    })


@api_view(['POST'])
def ledger_save(request):
    vendor_pk = request.data.get("vendor", None)
    date = request.data.get("date", None)
    milkcategory_pk = request.data.get("milktype", None)
    quantity = request.data.get("quantity", None)

    related_vendor = Vendor.objects.get(pk=vendor_pk)
    related_milkcategory = MilkCategory.objects.get(pk=milkcategory_pk)
    price = related_milkcategory.milkprice
    total = float(quantity) * float(price)
    path = request.path
    pathstr = str(path)

    g = vendorledger(
        related_vendor=related_vendor,
        date=date,
        related_milkcategory=related_milkcategory,
        price=price,
        quantity=quantity,
        total=total
    )

    g.save()
    current_url = "/ledger/" + str(vendor_pk) + "/"
    return Response({'url': current_url}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def ledger_delete(request):
    pk = request.data.get('ledger_pk')
    ledger_entry = vendorledger.objects.get(pk=pk)
    vendor_pk = ledger_entry.related_vendor.pk
    ledger_entry.delete()
    current_url = "/ledger/" + str(vendor_pk) + "/"
    return Response({'url': current_url})


# Add Customer - This is a Profile model (For Create Admin/Manager/Customer)
@api_view(['POST'])
def addcustomer(request):
    serializer = ProfileFormSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Customer MilkCategory
@api_view(['GET', 'POST'])
def customer_milk_category(request):
    cl = Profile.objects.only('user')
    if request.method == 'POST':
        serializer = CustomerMilkCategoryFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        serializer = CustomerMilkCategoryFormSerializer()
    return Response(serializer.data)


# Customer_page
@api_view(['GET'])
def Customer_page(request):
    customer = request.user
    customer_info = Customerledger.objects.filter(related_customer=customer)

    alltotal = 0.0
    for i in customer_info:
        alltotal = alltotal + float(i.total)
    print(alltotal)

    for data in customer_info:
        print("Customer Name: ", data.related_customer)
        print("joining Date: ", data.date)
        print("Quantity: ", data.price)
        print("Total: ", data.total)

    return Response({'customer_info': customer_info, 'alltotal': alltotal})


# Customer ledger
@api_view(['GET'])
def customer_ledger(request, pk):
    customer_obj = get_object_or_404(User, pk=pk)
    cus_user_info = Profile.objects.filter(user=customer_obj)
    customer_ledger_info = Customerledger.objects.filter(related_customer=customer_obj)
    milktypes = CustomerMilkCategory.objects.filter(related_customer=customer_obj)
    milk_list = [(milk.animalname + "-" + str(milk.milkprice), milk.pk) for milk in milktypes]

    customer_full_name = f"{customer_obj.first_name} {customer_obj.last_name}"
    alltotal = 0.0
    for i in customer_ledger_info:
        alltotal = alltotal + float(i.total)
    print(alltotal)

    return Response({
        "customer_full_name": customer_full_name,
        "milk_list": milk_list,
        "customer_obj": customer_obj,
        "customer_ledger_info": customer_ledger_info,
        "alltotal": alltotal,
    })


@api_view(['POST'])
def customer_ledger_save(request):
    customer_pk = request.data.get("customer", None)
    date = request.data.get("date", None)
    milk_pk = request.data.get("milktype", None)
    quantity = request.data.get("quantity", None)

    related_customer = User.objects.get(pk=customer_pk)
    related_milk_category = CustomerMilkCategory.objects.get(pk=milk_pk)
    price = related_milk_category.milkprice
    total = float(quantity) * float(price)

    data = Customerledger(
        related_customer=related_customer,
        date=date,
        related_milk_category=related_milk_category,
        quantity=quantity,
        price=price,
        total=total,
    )
    data.save()

    current_url = "/customer_ledger/" + str(customer_pk) + "/"
    return Response({'url': current_url}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def customer_ledger_delete(request):
    pk = request.data.get('customer_pk')
    customer_ledger_entry = Customerledger.objects.get(pk=pk)
    customer_ledger_entry.delete()
    customer_pk = customer_ledger_entry.related_customer.pk
    current_url = "/customer_ledger/" + str(customer_pk) + "/"
    return Response({'url': current_url})


@api_view(['GET'])
def allcustomer(request):
    customerinfo = Profile.objects.all()
    return Response(customerinfo)
