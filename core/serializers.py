from rest_framework import serializers
from drf_base64.fields import Base64ImageField
from .exceptions import *
from .models import User, Seller, Product, ProductSold, Client


class UserSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False)
    old_password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        password = validated_data.pop('password')

        validated_data['is_active'] = True

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        old_password = validated_data.pop('old_password', None)

        if password is not None and not instance.check_password(old_password):
            raise InvalidPassword

        if password is not None:
            instance.set_password(password)

        new_instance = super().update(instance, validated_data)

        return new_instance

    class Meta:
        model = User
        exclude = ('forgot_password_hash', 'forgot_password_expire')
        extra_kwargs = {'password': {'write_only': True},
                        'old_password': {'write_only': True}}
        read_only_fields = ('id', 'cpf')


class UserAdminSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False)
    old_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        exclude = ('forgot_password_hash', 'forgot_password_expire')
        extra_kwargs = {'password': {'write_only': True},
                        'old_password': {'write_only': True}}
        read_only_fields = ('id', 'cpf')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSold
        fields = '__all__'


class ProductSoldSerializerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSoldSerializer
        fields = '__all__'
