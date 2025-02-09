from django.db import models
from django.contrib.auth import get_user_model
import uuid
import logging


logger = logging.getLogger('ecommerce_project')

User = get_user_model()

def get_default_category():
    from shop.models import Category
    category, created = Category.objects.get_or_create(name="Default", description="Default category")
    return category.id

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, default=get_default_category)

    def save(self, *args, **kwargs):
        try:
            logger.info(f"Saving product: {self.name}")
            super().save(*args, **kwargs)
            logger.info(f"Product saved successfully: {self.name}")
        except Exception as e:
            logger.error(f"Error saving product: {str(e)}", exc_info=True)
            raise

    def soft_delete(self):
        try:
            logger.info(f"Soft deleting product: {self.name}")
            self.is_active = False
            self.deleted_at = models.DateTimeField(auto_now=True)
            self.save()
            logger.info(f"Product soft deleted: {self.name}")
        except Exception as e:
            logger.error(f"Error deleting product: {str(e)}", exc_info=True)
            raise

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def save(self, *args, **kwargs):
        try:
            logger.info(f"Saving category: {self.name}")
            super().save(*args, **kwargs)
            logger.info(f"Category saved successfully: {self.name}")
        except Exception as e:
            logger.error(f"Error saving category: {str(e)}", exc_info=True)
            raise

    def soft_delete(self):
        try:
            logger.info(f"Soft deleting category: {self.name}")
            self.is_active = False
            self.deleted_at = models.DateTimeField(auto_now=True)
            self.save()
            logger.info(f"Category soft deleted: {self.name}")
        except Exception as e:
            logger.error(f"Error deleting category: {str(e)}", exc_info=True)
            raise

    def __str__(self):
        return self.name
    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
