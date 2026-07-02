from django.db import models
import uuid
import secrets

from django.utils.text import slugify
from users.models import Profile

from .paystack import Paystack

# ::: CATEGORY :::
class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category',null=True,blank=True)
    created = models.DateTimeField( auto_now_add=True)
    def __str__(self):
        return self.title
    
# ::: PRODUCTS :::
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.BigIntegerField()
    discount_price = models.BigIntegerField(null=True,blank=True)
    main = models.ImageField(upload_to='products')
    image1 = models.ImageField(upload_to='products',null=True,blank=True)
    image2 = models.ImageField(upload_to='products',null=True,blank=True)
    image3 = models.ImageField(upload_to='products',null=True,blank=True)
    image4 = models.ImageField(upload_to='products',null=True,blank=True)
    image5 = models.ImageField(upload_to='products',null=True,blank=True)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    review = models.TextField()
    rating = models.IntegerField()
    in_stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    product_code = models.UUIDField(default=uuid.uuid4 ,unique=True,null=True, max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# ::: CART :::
class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    total = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile}'s Cart - Total: {self.total}"

# ::: CART PRODUCT :::
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        price = self.product.discount_price if self.product.discount_price else self.product.price
        return f"{self.product.title} - {self.quantity} * {price} = {self.quantity * price}"


# ORDER
ORDER_STATUS =(
    ('PENDING_ORDER','PENDING_ORDER'),
    ('ORDER_RECEIVED','ORDER_RECEIVED'),
    ('ORDER_CONFIRMED', 'ORDER_CONFIRMED'),
    ('ORDER_PROCESSED','ORDER_PROCESSED'),
    ('ORDER_SHIPPED','ORDER_SHIPPED'),
    ('ORDER_RETURNED', 'ORDER_RETURNED'),
    ('ORDER_DELIVERED','ORDER_DELIVERED')
               )

PAYMENT_METHOD = (
    ('paystack','paystack'),
    ('flutterwave','flutterwave'),
    ('cash_on_delivery', 'cash_on_delivery'),
    ('paypal','paypal')
)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    order_by = models.CharField(max_length=255)
    shipping_address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    subtotal = models.BigIntegerField()
    amount = models.BigIntegerField()
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS, default='PENDING_ORDER')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default='paystack')
    payment_completed = models.BooleanField(default=False)
    ref = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_by}'s Order - Status: {self.order_status} - Amount: {self.amount}"
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref=ref)
            if not obj_with_sm_ref:
                self.ref = ref
        super().save(*args, **kwargs)
    
    # convert from kobo to cent
    def amount_value(self):
        return self.amount * 100
    
    # verify payment
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref)
        if status and result.get('status') == "success":
            if result['amount'] /100 == self.amount:
                self.payment_completed = True
                self.save()
                return True, "Payment verified successfully"
            if self.payment_completed == True:
                self.cart = None
                self.save()
                return True, "Payment already verified"
            return False
        return False