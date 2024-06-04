from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.
class Order(models.Model):
    PROCESSING = 'PROCESSING'
    WORK = 'WORK'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

    STATUS_CHOICES = (
        (PROCESSING, "В обработке"),
        (WORK, "В работе"),
        (COMPLETED, "Исполнено"),
        (CANCELED, "Отменён"),
    )

    full_name = models.CharField(max_length=100, verbose_name="ФИО покупателя")
    email = models.CharField(max_length=50, verbose_name="Почта")
    mobile_number = models.CharField(max_length=20, verbose_name="Мобильный телефон")
    address = models.CharField(max_length=100, null=True, blank=True, default=None, verbose_name="Адрес покупателя")
    total_price = models.PositiveIntegerField(verbose_name="Итоговая стоимость")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PROCESSING)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    date_complete = models.DateField(null=True, blank=True, default=None, verbose_name="Дата выполнения")

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('order:chat', kwargs={'order_id': self.id})
