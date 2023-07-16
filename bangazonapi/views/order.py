from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

class OrderView(ViewSet):

    def retrieve(self, request, pk):
    
    
    def list(self, request):
