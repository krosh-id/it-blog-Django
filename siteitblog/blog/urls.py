from django.contrib import admin
from django.urls import path, register_converter
from . import converters
from .views import lenta, show_post, login, registration, profile_user, my_post

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', lenta, name='lenta'),
    path('post/<int:post_id>', show_post, name='post'),
    path('my-post/<int:profile_id>', my_post, name='my_post'),
    path('login', login, name='login'),
    path('registration', registration, name='registration'),
    path('profile/<int:profile_id>', profile_user, name='profile'),
]
