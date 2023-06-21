from rest_framework import serializers
from .models import User, Vendor, MilkCategory, Profile, CustomerMilkCategory, CustomerLedger, VendorLedger


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    subject = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True)
    message = serializers.CharField(required=True, max_length=1000)


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class AddVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('managername', 'vendorname', 'joiningdate', 'address', 'vendorcontact', 'status')


class MilkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkCategory
        fields = ('animalname', 'milkprice', 'related_vendor')


class VendorLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorLedger
        fields = ('related_vendor', 'related_milkcategory', 'date', 'price', 'quantity', 'total')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'user_type', 'contact_number', 'joining_data', 'address')


class CustomerMilkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMilkCategory
        fields = ('animalname', 'milkprice', 'related_customer')


class CustomerLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLedger
        fields = ('related_milk_category', 'related_customer', 'date', 'price', 'quantity', 'total')
