from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer, Invoice


class InvoiceAPITests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer", email="test@example.com"
        )

    def test_create_invoice(self):
        url = reverse("invoice-list-create")
        data = {
            "customer": self.customer.id,
            "issue_date": "2025-07-20",
            "due_date": "2025-08-20",
            "items": [{"description": "Item 1", "quantity": 2, "unit_price": 50.00}],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Invoice.objects.get().items.count(), 1)
