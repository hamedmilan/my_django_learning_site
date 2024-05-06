from django import template
from blog.models import Post, Category
from django.utils import timezone


register = template.Library()


@register.inclusion_tag('website/index-latestposts.html')
def index_latestposts(arg=6):
    posts = Post.objects.filter(status = True, published_date__lte=timezone.now()).order_by('-published_date')[:arg]

    return {'posts': posts}

