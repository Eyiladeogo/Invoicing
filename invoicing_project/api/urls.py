from django.urls import path
from .views import (
    CustomerListCreateAPIView,
    InvoiceListCreateAPIView,
    InvoiceDetailAPIView,
)

urlpatterns = [
    path(
        "customers/", CustomerListCreateAPIView.as_view(), name="customer-list-create"
    ),
    path("invoices/", InvoiceListCreateAPIView.as_view(), name="invoice-list-create"),
    path("invoices/<int:pk>/", InvoiceDetailAPIView.as_view(), name="invoice-detail"),
]
