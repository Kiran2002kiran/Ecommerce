from django.db import models
import uuid

class Payment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
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
        return self.transaction_id
