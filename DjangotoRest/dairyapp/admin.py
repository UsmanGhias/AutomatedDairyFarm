from rest_framework import serializers, viewsets
from dairyapp.models import Vendor, MilkCategory, vendorledger, Profile, CustomerMilkCategory, Customerledger

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendorname', 'managername', 'joiningdate', 'vendorcontact']

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class MilkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkCategory
        fields = ['animalname', 'milkprice', 'related_vendor']

class MilkCategoryViewSet(viewsets.ModelViewSet):
    queryset = MilkCategory.objects.all()
    serializer_class = MilkCategorySerializer

class VendorledgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendorledger
        fields = ['related_vendor', 'related_milkcategory', 'date', 'price', 'quantity', 'total']

class VendorledgerViewSet(viewsets.ModelViewSet):
    queryset = vendorledger.objects.all()
    serializer_class = VendorledgerSerializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['__str__', 'user_type', 'contact_number', 'address']

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class CustomerMilkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMilkCategory
        fields = ['fullname', 'animalname', 'milkprice']

class CustomerMilkCategoryViewSet(viewsets.ModelViewSet):
    queryset = CustomerMilkCategory.objects.all()
    serializer_class = CustomerMilkCategorySerializer

class CustomerledgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customerledger
        fields = ['related_customer', 'date', 'quantity', 'price', 'total']

class CustomerledgerViewSet(viewsets.ModelViewSet):
    queryset = Customerledger.objects.all()
    serializer_class = CustomerledgerSerializer

