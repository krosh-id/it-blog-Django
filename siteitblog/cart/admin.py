from django.contrib import admin
from django.utils.safestring import mark_safe

from cart.models import CategoryProduct, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'category', 'product_photo')
    ordering = ['-date_created', '-date_modified']
    readonly_fields = ['product_photo']
    list_per_page = 10
    # list_display_links = ('id', 'date_created') поля по котором возможен переход

    @admin.display(description='Фото')
    def product_photo(self, product: Product):
        if product.image:
            return mark_safe(f"<img src='{product.image.url}' width=50 ")
        return 'Без фото'


@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')