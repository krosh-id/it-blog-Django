from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'is_published', 'category', 'post_photo')
    ordering = ['-date_created', '-date_modified']
    readonly_fields = ['post_photo']
    list_editable = ('is_published', )
    list_per_page = 10
    # list_display_links = ('id', 'date_created') поля по котором возможен переход

    @admin.display(description='Фото')
    def post_photo(self, post: Post):
        if post.image:
            return mark_safe(f"<img src='{post.image.url}' width=50 ")
        return 'Без фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')