from django import template
from django.db.models import Count

from blog.models import Category

register = template.Library()


@register.simple_tag(name="getcats")
def get_categories():
    categories = Category.objects.annotate(total=Count('posts').filter(total__gt=0))
    return categories
