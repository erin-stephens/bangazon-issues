from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'uid', 'email', 'url', 'first_name', 'last_name', 'username')
