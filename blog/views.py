from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.views.generic.edit import CreateView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from easy_thumbnails.files import get_thumbnailer
from django.http import HttpResponse


def blog_home(request):
    posts = BlogPost.objects.order_by('-created')
    paginator = Paginator(posts, 10)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'post-ajax.html',
                      {'posts': posts})

    return render(request, 'blog-home.html',
                  {'posts': posts})


def post_content(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    posts = BlogPost.objects.order_by('-created').exclude(id=post.id)[:5]

    return render(request, 'blog-post.html',
                  {'post': post, 'recommended': posts})


class PostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'post-create.html'
    success_url = '/blog/'


class PostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'post-create.html'
    success_url = '/blog/'


def faq_page(request):

    return render(request, 'faq-page.html')


def download(request, f_type, pk):
    document = get_object_or_404(BlogPost, pk=pk)
    thumb = get_thumbnailer(document.image)[f_type]
    response = HttpResponse(thumb, content_type='image/png+jpeg')
    response['Content-Disposition'] = f'attachment; filename="{document.image.name}"'

    return response
