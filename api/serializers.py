from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Cake,AddtoCart,PlaceOrder,Reviews


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password"]

    def create(self, validated_data):
       return User.objects.create_user(**validated_data)
    
class ReviewSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Reviews
        fields=["id","user","comment","rating"]

    

class CakeSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    cake_review=ReviewSerializer(read_only=True,many=True)
    class Meta:
        model=Cake
        fields="__all__"


class CartSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    class Meta:
        model=AddtoCart
        # fields="__all__"
        exclude=("cake",)

class OrderSerializer(serializers.ModelSerializer):
    cake=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    expected_deliverydate=serializers.CharField(read_only=True)
    class Meta:
        model=PlaceOrder
        fields=["cake","user","created_date","status","expected_deliverydate","address","matter"]




