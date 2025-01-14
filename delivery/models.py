from django.db import models

class Delivery(models.Model):
    order_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')])
    updated_at = models.DateTimeField(auto_now=True)
