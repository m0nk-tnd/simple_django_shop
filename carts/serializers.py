from rest_framework import serializers

from products.serializers import ProductSerializer

from .models import Cart, CartProduct
from .utils import get_current_cart


class CartProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ["url", "id", "product", "count"]

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        super(CartProductAddSerializer, self).__init__(instance, data, **kwargs)
        self.context["cart"] = get_current_cart()

    def validate_product(self, value):
        # can update only same product
        if (
            not self.instance or self.instance.product != value
        ) and value in self.context["cart"].products.all():
            raise serializers.ValidationError("Product already in cart")
        return value

    def validate(self, data):
        if not self.context["cart"].is_editable:
            raise serializers.ValidationError("Can't edit this cart")
        if data["count"] > data["product"].stock:
            raise serializers.ValidationError("Not enough products in stock")
        return data

    def save(self, **kwargs):
        return super(CartProductAddSerializer, self).save(
            cart=self.context["cart"], **kwargs
        )


class CartProductSerializer(CartProductAddSerializer):
    product = ProductSerializer()


class CartSerializer(serializers.HyperlinkedModelSerializer):
    cartproduct_set = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "cartproduct_set"]
