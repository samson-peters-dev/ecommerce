from django.urls import reverse
from rest_framework import status,serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings

from .models import *
from . serializers import *

import requests

# ::: CATEGORY CRUD VIEW :::
class CategoryCreateRetrieveView(APIView):
    # ::: create
    def post(self,request):
        try:
            serializers = CategorySerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # :::retrieve all
    def get(self,request):
        try:
            categories = Category.objects.all()
            serializers = CategorySerializer(categories, many=True)
            return Response(serializers.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# ::: retrieve single , update, delete
class CategoryRUDView(APIView):
    # retrieve single
    def get(self,request,id):
        try:
            category = get_object_or_404(Category, id=id)
            serializers = CategorySerializer(category)
            return Response(serializers.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # update single
    def put(self,request,id):
        try:
            category = get_object_or_404(Category, id=id)
            serializers = CategorySerializer(category, data=request.data,partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status = status.HTTP_200_OK)
            return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # delete single
    def delete(self,request,id):
        try:
            category = get_object_or_404(Category, id=id)
            category.delete()
            return Response({"Message": "Category Deleted"}, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ::: PRODUCT CRUD VIEW :::
class ProductCreateRetrieveView(APIView):
    # ::: create
    def post(self,request):
        try:
            serializers = ProductSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # :::retrieve all
    def get(self,request):
        try:
            products = Product.objects.all()
            serializers = ProductSerializer(products, many=True)
            return Response(serializers.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# ::: retrieve single , update, delete
class ProductRUDView(APIView):
    # retrieve single
    def get(self,request,id):
        try:
            product = get_object_or_404(Product, id=id)
            serializers = ProductSerializer(product)
            return Response(serializers.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # update single
    def put(self,request,id):
        try:
            product = get_object_or_404(Product, id=id)
            serializers = ProductSerializer(product, data=request.data,partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status = status.HTTP_200_OK)
            return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # delete single
    def delete(self,request,id):
        try:
            product = get_object_or_404(Product, id=id)
            product.delete()
            return Response({"Message": "Product Deleted"}, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ADD TO CART
class AddToCartView(APIView):
    def post(self,request,id):
        try:
            # product to be added to cart
            product = get_object_or_404(Product, id=id)
            # create a cart session , anyone can add to cart
            cart_id = request.session.get('cart_id')
            # creating a price and discount price
            price = product.discount_price if product.discount_price else product.price
            
            while transaction.atomic():
                if cart_id:
                    cart = Cart.objects.filter(id=cart_id).first()
                    if cart is None:
                        cart= Cart.objects.create(total=0)
                        request.session['cart_id'] = cart.id
                    
                    # if there is a product in the cart before
                    product_in_cart = cart.cartproduct_set.filter(product=product)
                
                    if product_in_cart:
                        #increase the product quantity
                        cartproduct = product_in_cart.last()
                        cartproduct.quantity +=1
                        cartproduct.subtotal += price
                        cartproduct.save()
                        cart.total +=price
                        cart.save()
                        return Response({'message': 'product quantity increased'}, status=status.HTTP_200_OK)
                    else:
                        # create it as a new product
                        cartproduct = CartProduct.objects.create(cart=cart, product=product, quantity=1, subtotal=price)
                        cartproduct.save()
                        cart.total +=price
                        cart.save()
                        return Response({'message': 'product added to cart'}, status=status.HTTP_200_OK)
                else:
                    # create a new cart and cart product
                    cart = Cart.objects.create(total=0)
                    request.session['cart_id'] = cart.id
                    cartproduct = CartProduct.objects.create(cart=cart,product=product,quantity=1,subtotal=price)
                    cartproduct.save()
                    cart.total +=price
                    cart.save()
                    return Response({'message': 'A new cart created with product'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# USERS CART
class MyCartView(APIView):
    def get(self,request):
        try:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = get_object_or_404(Cart, id=cart_id)
                return Response({"Message":f"Pofile -  {cart.id}"})
            return Response({"Message":f"No Pofile"})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# MANAGE USERS CART
class ManageCartView(APIView):
    def post(self,request,id):
        action = request.data.get('action')
        if action not in ['inc', 'dcr', 'rmv']:
            return Response({'message': 'Invalid Action'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart_obj = CartProduct.objects.get(id=id)
            cart = cart_obj.cart
            price = cart_obj.product.discount_price if cart_obj.product.discount_price else cart_obj.product.price

            if action == "inc":
                cart_obj.quantity += 1
                cart_obj.subtotal += price
                cart_obj.save()
                cart.total += price
                cart.save()
                return Response({'message': 'Quantity Increased'})
            if action == "dcr":
                cart_obj.quantity-=1
                cart_obj.subtotal -= price
                cart_obj.save()
                cart.total -= price
                cart.save()
                if cart_obj.quantity == 0:
                    cart_obj.delete()
                    return Response({'message': 'Product Removed from Cart'})
                return Response({'message': 'Quantity Decreased'})
            if action == "rmv":
                cart.total -= price
                cart.save()
                cart_obj.delete()
                return Response({'message': 'Product Removed from Cart'})

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# CHECKOUT CART
class CheckoutCartView(APIView):
    def post(self,request):
        try:
            cart_id = request.session.get('cart_id', None)
            if cart_id is None:
                return Response({'message': 'No cart to checkout'}, status=status.HTTP_400_BAD_REQUEST)
            cart_obj = get_object_or_404(Cart, id=cart_id)

            serializers = CheckoutSerializer(data=request.data)
            if serializers.is_valid():
                order = serializers.save(
                    cart = cart_obj,
                    subtotal = cart_obj.total,
                    amount = cart_obj.total
                )
                del request.session['cart_id']
                # if order.payment_method == 'cash_on_delivery':
                #     payment_url = reverse('pod_page', args=[order.id])
                #     return Response({"Redirect Page Url": payment_url}, status=status.HTTP_200_OK)
                if order.payment_method == 'paystack':
                    payment_url = reverse('paystack_page', args=[order.id])
                    return Response({"Redirect Page Url": payment_url}, status=status.HTTP_200_OK)
                return Response({'message': f'Order Placed Successfully, Your Order Number is {order.id}'}, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class PaymentOnDelieveryView(APIView):
#     pass

# PAYMENT VERIFICATION
class PaymentView(APIView):
    def get(self,request,id):
        try:
            order = get_object_or_404(Order, id =id)
            if Order is None:
                return Response({'message': 'No Order Found'}, status=status.HTTP_400_BAD_REQUEST)
            
            url = "https://api.paystack.co/transaction/initialize"
            headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
            }
            data = {
                "amount": order.amount * 100,
                "email": order.email,
                "reference":order.ref
            }
            response = requests.post(url,data=data,headers=headers)
            response_data = response.json()

            if response_data["status"]:
                paystack_url = response_data["data"]
                return Response({
                    "order": order.id,
                    'total': order.amount,
                    "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY,
                    "payment_url": paystack_url
                    
                },status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Payment Initialization Failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# PAYMENT VERIFICATION
class VerifyPaymentView(APIView):
    def get(self,request,ref):
        try:
            order = get_object_or_404(Order, ref=ref)
            url = f"https://api.paystack.co/transaction/verify/{ref}"
            headers = headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
            }
            response = requests.get(url, headers=headers)
            response_data = response.json()

            if response_data["status"] and response_data['data']['status'] == "success":
                order.payment_completed = True
                order.order_status = 'ORDER_RECEIVED'
                order.save()
                return Response({'message': 'Payment Verified Successfully'}, status=status.HTTP_200_OK)
            
            elif response_data['data']['status'] == "abandoned":
                order.order_status = 'PAYMENT_FAILED'
                order.save()
                return Response({'message': 'Payment was not completed'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Payment Failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)