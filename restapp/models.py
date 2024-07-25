from django.db import models
from django.contrib.auth.models import AbstractUser

class Cargo(models.Model):
    application_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Номер заявки")
    supplier = models.CharField(max_length=255, blank=True, null=True, verbose_name="Поставщик")
    recipient = models.CharField(max_length=255, blank=True, null=True, verbose_name="Получатель")
    cargo_description = models.TextField(blank=True, null=True, verbose_name="Груз")
    cargo_weight = models.FloatField(blank=True, null=True, verbose_name="Масса груза")
    contract_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="№ договора")
    delivery_date = models.CharField(max_length=100, blank=True, null=True, verbose_name="Дата поставки")
    vehicle_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Тип ТС")
    vehicle_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Номер ТС")
    shipment_date = models.CharField(max_length=100, blank=True, null=True, verbose_name="Дата отгрузки")
    arrival_date = models.CharField(max_length=100, blank=True, null=True, verbose_name="Дата поставки")

    def __str__(self):
        return self.application_number if self.application_number else 'Без номера заявки'


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.TextField(blank=True, null=True) 

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    def __str__(self):
        return self.username