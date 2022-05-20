from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"report", views.ReportViewSet, basename="report")
router.register(r"", views.OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
