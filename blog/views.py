from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def blog_view(request, **kwargs):
    posts = Post.objects.filter(status = True)
    
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name = kwargs['cat_name'])

    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username = kwargs['author_username'])

    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in = [kwargs['tag_name']])

    posts = posts.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
    posts = Paginator(posts, 3)

    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.page(1)
    except EmptyPage:
        posts = posts.page(1)

    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)

def single_view(request, pid):
    posts = Post.objects.filter(status = True, published_date__lte=timezone.now()).order_by('published_date')
    
    the_post = get_object_or_404(posts, id=pid)
    the_post.counted_view += 1
    the_post.save()

    next_post = posts.filter(published_date__gt=the_post.published_date)

    if next_post.count() != 0:
        next_post = next_post.order_by('published_date').first()
    else:
        next_post = 0


    previous_post = posts.filter(published_date__lt=the_post.published_date)

    if previous_post.count()!= 0:
        previous_post = previous_post.order_by('-published_date').first()
    else:
        previous_post = 0
        

    context = {'post': the_post, 'next_post': next_post, 'previous_post': previous_post}

    return render(request, 'blog/blog-single.html',context)


def blog_search(request):
    posts = Post.objects.filter(status = True)

    if request.method == 'GET':
        if r := request.GET.get('s'):
            posts = posts.filter(content__contains=r)
        
    posts = posts.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {'posts': posts}

    return render(request, 'blog/blog-home.html', context)

#def test_view(request):
#
#    return render(request, 'test.html')



