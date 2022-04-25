from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Calculation, Test, Parameter


@receiver(post_save, sender=Test)
def create_calculation(sender, instance, created, **kwargs):
    if created:
        Calculation.objects.create(test=instance, parameter=Parameter.objects.get(id=1))
        Calculation.objects.create(test=instance, parameter=Parameter.objects.get(id=2))
        Calculation.objects.create(test=instance, parameter=Parameter.objects.get(id=3))
        Calculation.objects.create(test=instance, parameter=Parameter.objects.get(id=4))
