import requests

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import Post, Commentary


def index(request):
    context = {'latest_post_list': Post.objects.order_by('-pub_date')[:5]}
    return render(request, 'index.html', context)


def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'full_post.html', {'post': post})


def send_commentary(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.POST['author'] not in ['', None] and request.POST['content'] not in ['', None]:
        post.commentary_set.create(
                                    content=request.POST['content'],
                                    author=request.POST['author'],
                                    pub_date=timezone.now()
                                  )
        return HttpResponseRedirect(reverse('post', args=(post.id,)))
    else:
        print("error")
        return render(request, 'full_post.html', {
            'post': post,
            'error_message': 'Error while sending comment, please check if each field is correctly filled.',
        })


def post_commentaries(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_commentaries.html', {'post': post})


def commentary(request, commentary_id):
    commentary = get_object_or_404(Commentary, pk=commentary_id)
    return render(request, 'commentary_wrapper.html', {'commentary': commentary})
