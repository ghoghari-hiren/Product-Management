from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Product, ProductLog

@receiver(post_save, sender=Product)
def log_product_save(sender, instance, created, **kwargs):
    user = getattr(instance, '_modified_by', None)
    ProductLog.objects.create(
        action="created" if created else "updated",
        product_id=instance.id,
        user=user
    )


@receiver(pre_delete, sender=Product)
def log_product_delete(sender, instance, **kwargs):
    user = getattr(instance, '_modified_by', None)

    ProductLog.objects.create(
        product_id=instance.id,
        action='delete',
        user=user,
        changes={
            "title": instance.title,
            "price": float(instance.price),
            "ssn": instance.ssn
        }
    )

