from django.db import models
from django.urls import reverse


class CategoryProduct(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории товара")
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория товаров"
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название товара")
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.TextField(max_length=500, verbose_name="Описание товара")
    processing_date = models.DateField(null=True, blank=True, verbose_name="Срок принятия заказа")
    image = models.ImageField(upload_to='photos_product/%Y/%m/%d/', default=None, null=True, blank=True,
                              verbose_name='Изображение')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name="products")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-date_created']

    def get_absolute_url(self):
        return reverse('product', kwargs={'post_id': self.id})
