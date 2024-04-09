from django.contrib import admin
from .models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'is_published', 'category')
    ordering = ['-date_created', '-date_modified']
    list_editable = ('is_published', )
    list_per_page = 10
    # list_display_links = ('id', 'date_created') поля по котором возможен переход


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')