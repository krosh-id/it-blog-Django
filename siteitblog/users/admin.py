from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import User

admin.site.register(User, UserAdmin)


# @admin.register(User)
# class User(admin.ModelAdmin):
#     list_display = ('id', 'username', 'first_name', 'last_name', 'user_photo')
#     list_display_links = ('id', 'username')
#
#     @admin.display(description='Фото')
#     def user_photo(self, user: User):
#         if user.photo:
#             return mark_safe(f"<img src='{user.photo.url}' width=50 ")
#         return 'Без фото'
