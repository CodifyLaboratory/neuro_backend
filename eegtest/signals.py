from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Calculation, Test


@receiver(post_save, sender=Test)
def create_calculation(sender, instance, created, **kwargs):
    if created:
        Calculation.objects.create(test=instance)
