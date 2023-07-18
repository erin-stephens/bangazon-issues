from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Product, User, Category

class ProductView(ViewSet):

    def retrieve(self, request, pk):
        
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    
    def list(self, request):
        
        products = Product.objects.all()
        seller_products = request.query_params.get('user_id', None)
        if seller_products is not None:
            products = products.filter(user_id=seller_products)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        
        seller = User.objects.get(pk=request.data["userId"])
        category = Category.objects.get(pk=request.data["categoryId"])
        product = Product.objects.create(
            seller_id=seller,
            category_id=category,
            title=request.data["title"],
            description=request.data["description"],
            quantity=request.data["quantity"],
            price=request.data["price"],
            image_url=request.data["imageUrl"]
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)
        
    def update(self, request, pk):
        
        product = Product.objects.get(pk=pk)
        seller = User.objects.get(pk=request.data["userId"])
        product.seller = seller
        category = Category.objects.get(pk=request.data["categoryId"])
        product.category=category
        product.title = request.data["title"]
        product.description = request.data["description"]
        product.quantity = request.data["quantity"]
        product.price=request.data["price"]
        product.image_url=request.data["imageUrl"]
        product.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ('id', 'seller', ' category', 'title', 'description', 'quantity', 'price', 'image_url')
