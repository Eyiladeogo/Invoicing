from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200) 
    email = models.EmailField(unique=True) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ) 

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices') 
    issue_date = models.DateField() 
    due_date = models.DateField() 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Invoice #{self.id} for {self.customer.name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items') 
    description = models.TextField() 
    quantity = models.IntegerField() 
    unit_price = models.DecimalField(max_digits=10, decimal_places=2) 

    @property
    def total(self):
        return self.quantity * self.unit_price 

    def __str__(self):
        return self.description