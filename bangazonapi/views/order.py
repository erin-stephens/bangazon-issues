from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Order, User, OrderProduct
from rest_framework.decorators import action

class OrderView(ViewSet):

    def retrieve(self, request, pk):
    
        try: 
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        customer = User.objects.get(pk=request.data["userId"])
        order = Order.objects.create(
            customer=customer,
            completed = request.data["completed"],
            total = request.data["total"],
            payment_type = request.data["paymentType"]
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def update(self, request, pk):
        order = Order.objects.get(pk=pk)
        customer = User.objects.get(pk=request.data["userId"])
        order.customer=customer
        order.completed = request.data["completed"]
        order.total = request.data["total"]
        order.payment_type = request.data["paymentType"]
        order.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def check_order(self, request, pk):
        try:
            order = OrderProduct.objects.get(
                order_id = pk,
                product_id = pk
            )
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(False)
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'customer', 'total', 'payment_type')
