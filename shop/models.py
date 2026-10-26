from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
 
 
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
 
    def __str__(self):
        return self.username
 
 
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
 
    def __str__(self):
        return self.name
 
 
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products'
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name
 
 
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'Корзина пользователя {self.user.username}'
 
 
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
 
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product'], name='unique_cart_product'
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name='cart_quantity_gte_1'
            ),
        ]
 
 
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('preparing', 'Готовится'),
        ('delivering', 'Доставляется'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='orders'
    )
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'Заказ №{self.pk}'
 
 
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    product_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
 
    def __str__(self):
        return f'{self.product_name} × {self.quantity}' 

