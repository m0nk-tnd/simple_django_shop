from rest_framework import status, viewsets
from rest_framework.response import Response

from .enums import ProductStatusEnum
from .models import Product
from .serializers import ProductPatchSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status=ProductStatusEnum.NORMAL).all()
    serializer_class = ProductSerializer
    patch_serializer_class = ProductPatchSerializer

    def destroy(self, request, *args, **kwargs):
        instance: Product = self.get_object()
        instance.status = ProductStatusEnum.ARCHIVED
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if kwargs.get("partial"):
            serializer_class = self.patch_serializer_class
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def _allowed_methods(self):
        methods = super(ProductViewSet, self)._allowed_methods()
        if "PUT" in methods:
            methods.remove("PUT")
        return methods
