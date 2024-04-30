from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


# обобщённая модель для привязки лайков
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Comment(models.Model):
    liked = False

    text = models.TextField(max_length=155, verbose_name='Комментарий')
    image = models.ImageField(upload_to='photos_comments/%Y/%m/%d/', default=None, null=True, blank=True,
                              verbose_name='Изображение')
    date_created = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comment')
    likes = GenericRelation(Like)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.post.id})

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def get_likes(self):
        user = get_user_model()
        obj_type = ContentType.objects.get_for_model(self)
        return user.objects.filter(
            likes__content_type=obj_type, likes__object_id=self.id)

    def get_is_liked(self, user):
        self.liked = self.likes.filter(user=user).exists()
        return self.liked



class Post(models.Model):
    liked = False

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    # slug = models.SlugField(max_length=255, unique=True, db_index=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLISHED)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    text = models.TextField(default=None, max_length=500)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, null=True, blank=True,
                              verbose_name='Изображение')

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    likes = GenericRelation(Like)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['-date_created'])
        ]

    def __str__(self):
        return str(self.author)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.id})

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def get_likes(self):
        user = get_user_model()
        obj_type = ContentType.objects.get_for_model(self)
        return user.objects.filter(
            likes__content_type=obj_type, likes__object_id=self.id)

    def get_is_liked(self, user):
        self.liked = self.likes.filter(user=user).exists()
        return self.liked

    @property
    def total_comments(self):
        return self.comment.count()
