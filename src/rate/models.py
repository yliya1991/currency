from django.db import models
from django.utils import timezone

from rate import model_choices as mch
from rate.utils import to_decimal


tz = timezone.get_default_timezone()


class Rate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)
    currency_type = models.PositiveSmallIntegerField(choices=mch.CURRENCY_TYPE_CHOICE)
    type = models.PositiveSmallIntegerField(choices=mch.RATE_TYPE_CHOICE) # noqa

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.amount = to_decimal(self.amount)

    def get_date(self):
        return f'{self.created.astimezone(tz).strftime("%d.%m.%Y %H:%M")}'
