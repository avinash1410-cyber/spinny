from rest_framework import serializers
from .models import Account,Box
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','id']

class AccountSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Account
        fields='__all__'

class BoxSerializer(serializers.ModelSerializer):
    Creator=AccountSerializer()
    class Meta:
        model=Box
        fields='__all__'


class BoxSerializer2(serializers.ModelSerializer):
    class Meta:
        model=Box
        fields=['Height','Length','Width','Area','Volume']