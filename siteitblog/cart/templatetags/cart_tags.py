from django import template
from django.db.models import Count

from cart.models import CategoryProduct

register = template.Library()


@register.simple_tag(name="getcatsproduct")
def get_categories_products():
    categories = CategoryProduct.objects.all()
    # annotate(total=Count('posts').filter(total__gt=0))
    return categories
