from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin
from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework import authentication,permissions
from django.contrib.auth.models import User
from api.serializers import UserSerializer,CakeSerializer,CartSerializer,OrderSerializer,ReviewSerializer
from api.models import Cake,AddtoCart,PlaceOrder,Reviews
from rest_framework.response import Response
from rest_framework.decorators import action


# Create your views here

class UserView(GenericViewSet,CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class CakeView(GenericViewSet,ListModelMixin,RetrieveModelMixin):
    serializer_class=CakeSerializer
    queryset=Cake.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        qs=Cake.objects.all()

        if "layers" in self.request.query_params:
            lay=self.request.query_params.get("layers")
            qs=qs.filter(layers=lay)

        if "shape" in self.request.query_params:
            shp=self.request.query_params.get("shape")
            qs=qs.filter(shape=shp)
        return qs
    @action(methods=["post"],detail=True)
    def addto_cart(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        cake=Cake.objects.get(id=id)
       
        
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            # qs=Cart.objects.create(cake=cake,user=request.user,quantity=serializer.validated_data.get("quantity"))
            # serializer=CartSerializer(qs)
            serializer.save(cake=cake,user=request.user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
    #localhost:8000/api/cakes/2/make_order/
    # method:post
    @action(methods=["post"],detail=True)
    def make_order(self,request,*args,**kwargs):
        cake=self.get_object()
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cake=cake,user=request.user)
            # qs=Order.objects.create(cake=cake,
            #                         user=request.user,
            #                         address=serializer.validated_data.get("address"),
            #                         matter=serializer.validated_data.get("matter"),

            #                         )
            # serializer=OrderSerializer(qs)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    @action(methods=["POST"],detail=True)
    def add_review(self,request,*args,**kwargs):
        serializer=ReviewSerializer(data=request.data)
        id=kwargs.get("pk")
        cak=Cake.objects.get(id=id)
        user=request.user
        if serializer.is_valid():
            serializer.save(user=user,cake=cak)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
class CartListView(GenericViewSet,ListModelMixin):
    queryset=AddtoCart.objects.all()
    serializer_class=CartSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return AddtoCart.objects.filter(user=self.request.user)


class OrderListView(GenericViewSet,ListModelMixin):
    querset=PlaceOrder.objects.all()
    serializer_class=OrderSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return PlaceOrder.objects.filter(user=self.request.user)
    
class ReviewListView(GenericViewSet,ListModelMixin):
    querset=PlaceOrder.objects.all()
    serializer_class=ReviewSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Reviews.objects.filter(user=self.request.user)

