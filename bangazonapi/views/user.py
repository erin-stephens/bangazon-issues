from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User, Order
from rest_framework.decorators import action

class UserView(ViewSet):
  
    def retrieve(self, request, pk):

        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def list(self, request):
      
      users = User.objects.all()
      serializer = UserSerializer(users, many=True)
      return Response(serializer.data)
    
    def destroy(self, request, pk):
        
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get'], detail=True)
    def getorder(self,request, pk):
        '''request to get users open order'''
        try: 
            order = Order.objects.get(
                customer_id = pk,
                completed = False
            )
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(False)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'customer', 'total', 'payment_type', 'completed')
        depth = 1
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'uid', 'email', 'url', 'first_name', 'last_name', 'username')
