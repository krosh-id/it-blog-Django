from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


def get_default_reaction():
    return {"like": 0, "lightning": 0, "comments": 0}


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


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

    text = models.TextField(max_length=155, verbose_name='Комментарий')
    image = models.ImageField(upload_to='photos_comments/%Y/%m/%d/', default=None, null=True, blank=True,
                              verbose_name='Изображение')
    reaction = models.JSONField(null=True, blank=True, default=get_default_reaction)
    date_created = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comment')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.post.id})


class Post(models.Model):
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
    reaction = models.JSONField(null=True, blank=True, default=get_default_reaction)

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')

    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['-date_created'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.id})
