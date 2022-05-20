from rest_framework import serializers
from django.db import transaction

from carts.serializers import CartSerializer
from carts.utils import get_current_cart

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()

    class Meta:
        model = Order
        fields = ["id", "cart", "status", "created_at", "updated_at", "name"]


class OrderAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["name"]

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        super(OrderAddSerializer, self).__init__(instance, data, **kwargs)
        self.context["cart"] = get_current_cart()

    def validate(self, data):
        if self.context["cart"].products.count() == 0:
            raise serializers.ValidationError("Your cart is empty")
        return data

    @transaction.atomic
    def save(self, **kwargs):
        cart = self.context["cart"]
        # fix prices in order cart
        for cart_product in cart.cartproduct_set.all():
            cart_product.cost = cart_product.product.cost
            cart_product.price = cart_product.product.price
            cart_product.save()
            cart_product.product.stock -= cart_product.count
            cart_product.product.save()
        cart.is_editable = False
        cart.save()
        return super(OrderAddSerializer, self).save(cart=self.context["cart"], **kwargs)


class ReportInSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ReportOutSerializer(serializers.Serializer):
    cart__products__title = serializers.CharField(read_only=True)
    revenue = serializers.IntegerField(read_only=True)
    profit = serializers.IntegerField(read_only=True)
    count = serializers.IntegerField(read_only=True)
    cancel_count = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
