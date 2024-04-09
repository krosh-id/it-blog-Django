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


class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    author = models.PositiveIntegerField()
    # slug = models.SlugField(max_length=255, unique=True, db_index=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLISHED)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    text = models.TextField(default=None, max_length=500)
    img = models.CharField(max_length=255, null=True, blank=True) # изменить потом
    reaction = models.JSONField(null=True, blank=True, default=get_default_reaction)

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

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_slug': self.slug})

