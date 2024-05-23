from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import CommenttForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
 

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
    if request.method == 'POST':
        form = CommenttForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment has been submitted successfully!')
        else:
            messages.add_message(request, messages.ERROR, 'Your comment has not been submitted successfully!')


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
        
    
    if not the_post.login_required:

        comments = Comment.objects.filter(post=the_post.id, approved=True)

        form = CommenttForm()

        context = {'post': the_post, 'next_post': next_post, 'previous_post': previous_post, 'comments': comments, 'form': form}

        return render(request, 'blog/blog-single.html',context)
    else:
        return HttpResponseRedirect(reverse('accounts:login'))




def blog_search(request):
    posts = Post.objects.filter(status = True)

    if request.method == 'GET':
        if r := request.GET.get('s'):
            posts = posts.filter(content__contains=r)
        
    posts = posts.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {'posts': posts}

    return render(request, 'blog/blog-home.html', context)





