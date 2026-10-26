from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Category, Product, Cart, CartItem, Order, OrderItem
)
 
 
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Контакты', {'fields': ('phone', 'address')}),
    )
 
 
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
 
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name',)
 
 
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
 
 
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]
 
 
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity')
 
 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'status', 'total', 'created_at')
    list_filter = ('status',)
    readonly_fields = (
        'user', 'customer_name', 'phone', 'address', 'total',
        'created_at'
    )
    inlines = [OrderItemInline]
