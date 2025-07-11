from rest_framework import serializers
from .models import Customer, Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = InvoiceItem
        fields = ("id", "description", "quantity", "unit_price", "total")


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = (
            "id",
            "customer",
            "issue_date",
            "due_date",
            "status",
            "items",
            "total_amount",
        )

    def get_total_amount(self, obj):
        return sum(item.total for item in obj.items.all())

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        if not items_data:
            raise serializers.ValidationError(
                "Invoice must have at least one line item."
            )
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice

    def validate(self, data):
        if data["issue_date"] > data["due_date"]:
            raise serializers.ValidationError("Due date must be after issue date.")
        return data

    def update(self, instance, validated_data):
        # Pop the nested 'items' data if it exists
        items_data = validated_data.pop("items", None)

        # Update the fields on the Invoice instance
        instance.customer = validated_data.get("customer", instance.customer)
        instance.issue_date = validated_data.get("issue_date", instance.issue_date)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.status = validated_data.get("status", instance.status)
        instance.save()

        # If items_data is provided, handle the nested InvoiceItem updates
        if items_data is not None:
            # Delete old items
            instance.items.all().delete()
            # Create new items
            for item_data in items_data:
                InvoiceItem.objects.create(invoice=instance, **item_data)

        return instance


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "created_at")
