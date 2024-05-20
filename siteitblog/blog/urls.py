from django.urls import path, register_converter
from . import converters
from .views import LentaView, \
    ShowPostView, ProfileView, ShowByCategoryView, LikePostView, LikeCommentView, AboutCompanyView

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', LentaView.as_view(), name='lenta'),
    path('post/<int:post_id>', ShowPostView.as_view(), name='post'),
    path('category/<slug:cat_slug>', ShowByCategoryView.as_view(), name='category'),
    path('profile/<int:profile_id>', ProfileView.as_view(), name='profile'),
    path('post/like', LikePostView.as_view(), name='like-post'),
    path('comment/like', LikeCommentView.as_view(), name='like-comment'),
    path('about_company', AboutCompanyView.as_view(), name='about_company'),
]
