from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Product, User, Category, Order, OrderProduct
from rest_framework.decorators import action

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
            
        
        order_id = request.query_params.get('order', None)
        if order_id is not None:
            try:
                order = Order.objects.get(pk=order_id)
                for product in products:
                    product.added = len(OrderProduct.objects.filter(order=order, product=product)) > 0
            except Order.DoesNotExist:
                pass  # Handle the case when the order doesn't exist

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        
        seller = User.objects.get(uid=request.data["userId"])
        category = Category.objects.get(pk=request.data["category"])
        product = Product.objects.create(
            seller=seller,
            category=category,
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
        seller = User.objects.get(uid=request.data["userId"])
        product.seller = seller
        category = Category.objects.get(pk=request.data["category"])
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
    
    @action(methods=['post'], detail=True)
    def addtocart(self, request, pk):
        order = Order.objects.get(pk=request.data["orderId"])
        product = Product.objects.get(pk=request.data["productId"])
        cart = OrderProduct.objects.create(
            order=order,
            product=product
        )
        return Response({'message': 'Product added to order'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def remove(self, request, pk):
        order = Order.objects.get(pk=["orderId"])
        product = Product.objects.get(pk=["productId"])
        order_products = OrderProduct.objects.get(
            order_id=order.id,
            product_id=product.id
        )
        order_products.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ('id', 'seller', 'category', 'title', 'description', 'quantity', 'price', 'image_url', 'added')
        depth = 1
