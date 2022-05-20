from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .models import Cart, CartProduct
from .serializers import CartProductAddSerializer, CartProductSerializer, CartSerializer
from .utils import get_current_cart


class CartViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        # it's not a list but retrieve current cart
        instance = get_current_cart()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CartProductViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    add_serializer_class = CartProductAddSerializer

    def get_queryset(self):
        cart = get_current_cart()
        return CartProduct.objects.filter(cart=cart).all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return self.add_serializer_class
        return self.serializer_class
