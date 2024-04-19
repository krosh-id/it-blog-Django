from django.contrib import admin
from django.urls import path, register_converter
from . import converters
from .views import login, registration, usefully_resource, LentaView, \
    ShowPostView, ShowMyPostsView, ShowByCategoryView, ProfileView

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', LentaView.as_view(), name='lenta'),
    path('post/<int:post_id>', ShowPostView.as_view(), name='post'),
    path('category/<slug:cat_slug>', ShowByCategoryView.as_view(), name='category'),
    path('my-post/<int:profile_id>', ShowMyPostsView.as_view(), name='my-post'),
    path('login', login, name='login'),
    path('registration', registration, name='registration'),
    path('profile/<int:profile_id>', ProfileView.as_view(), name='profile'),
    path('usefully-resource', usefully_resource, name='resource'),
]
