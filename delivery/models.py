from django.db import models
import uuid

class Delivery(models.Model):
    order_id = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50, 
        choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')]
    )
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = models.DateTimeField(auto_now=True)
        self.save()

    def __str__(self):
        return self.order_id
