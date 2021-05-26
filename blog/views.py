from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Post


def index_blog(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'blog/index_blog.html',
                  {'posts': posts,
                   'page': page, 'paginator': paginator})


def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post.html', {'post': post})
