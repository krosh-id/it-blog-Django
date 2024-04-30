from django.urls import path, register_converter
from . import converters
from .views import LentaView, \
    ShowPostView, ShowMyPostsView, ProfileView, ShowByCategoryView, LikePostView, LikeCommentView

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', LentaView.as_view(), name='lenta'),
    path('post/<int:post_id>', ShowPostView.as_view(), name='post'),
    path('category/<slug:cat_slug>', ShowByCategoryView.as_view(), name='category'),
    path('my-post/<int:profile_id>', ShowMyPostsView.as_view(), name='my-post'),
    path('profile/<int:profile_id>', ProfileView.as_view(), name='profile'),
    path('post/like', LikePostView.as_view(), name='like-post'),
    path('comment/like', LikeCommentView.as_view(), name='like-comment'),
]
