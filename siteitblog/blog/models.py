from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 1, 'Черновик'
        PUBLISHED = 2, 'Опубликовано'

    author = models.PositiveIntegerField()
    # slug = models.SlugField(max_length=255, unique=True, db_index=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    text = models.TextField(default=None, max_length=1000)
    img = models.CharField(max_length=255, null=True) # изменить потом
    reaction = models.JSONField(null=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')

    def __str__(self):
        return self.author

    class Meta:
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['-date_created'])
        ]

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_slug': self.slug})

