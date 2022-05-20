from django.db.models import Q, Sum
from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .enums import OrderStatusEnum
from .models import Order
from .serializers import (
    OrderAddSerializer,
    OrderSerializer,
    ReportInSerializer,
    ReportOutSerializer,
)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    add_serializer_class = OrderAddSerializer

    def get_serializer_class(self):
        if self.action in ["create"]:
            return self.add_serializer_class
        return self.serializer_class

    @transaction.atomic
    @action(detail=True)
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status == OrderStatusEnum.CANCELED:
            raise APIException("Order is canceled already")
        order.status = OrderStatusEnum.CANCELED

        order.save()
        serializer = self.get_serializer(order)
        for cart_product in order.cart.cartproduct_set.all():
            cart_product.product.stock += cart_product.count
            cart_product.product.save()
        return Response(serializer.data)

    @transaction.atomic
    @action(detail=True)
    def deliver(self, request, pk=None):
        order = self.get_object()
        if order.status != OrderStatusEnum.PROCESSING:
            raise APIException("Order is processed already")
        order.status = OrderStatusEnum.DELIVERED

        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class ReportViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ReportInSerializer

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # create query with grouping and aggregation for report
        query = (
            Order.objects.filter(
                updated_at__gte=data["start_date"],
                updated_at__lte=data["end_date"],
                status__in=(OrderStatusEnum.CANCELED, OrderStatusEnum.DELIVERED),
            )
            .values("cart__products__id", "cart__products__title")
            .annotate(
                revenue=Sum(
                    "cart__cartproduct__cost",
                    filter=Q(status=OrderStatusEnum.DELIVERED),
                ),
                profit=Sum(
                    "cart__cartproduct__price",
                    filter=Q(status=OrderStatusEnum.DELIVERED),
                )
                - Sum(
                    "cart__cartproduct__cost",
                    filter=Q(status=OrderStatusEnum.DELIVERED),
                ),
                count=Sum(
                    "cart__cartproduct__count",
                    filter=Q(status=OrderStatusEnum.DELIVERED),
                ),
                cancel_count=Sum(
                    "cart__cartproduct__count",
                    filter=Q(status=OrderStatusEnum.CANCELED),
                ),
            )
            .order_by("cart__products__id")
        )
        objects = query.all()
        result = ReportOutSerializer(instance=objects, many=True)
        return Response(result.data, status=status.HTTP_200_OK)
