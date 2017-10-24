import requests

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone

from .models import Post, Commentary


def index(request):
    posts = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    return render(request, 'index.html', {'latest_post_list': posts})


def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.pub_date > timezone.now():
        raise Http404("Page not found")
    return render(request, 'full_post.html', {'post': post})


def send_commentary(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.POST['author'] not in ['', None] and request.POST['content'] not in ['', None]:

        ''' reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response,
        }
        print(data)
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''

        if result['success']:
            post.commentary_set.create(
                                        content=request.POST['content'],
                                        author=request.POST['author'],
                                        pub_date=timezone.now()
                                      )
            return HttpResponseRedirect(reverse('post', args=(post.id,)))
        else:
            return render(request, 'full_post.html', {
                'post': post,
                'error_message': result,
                'author': request.POST['author'],
                'content': request.POST['content'],
            })
    else:
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


def search(request):
    query = request.POST['search']
    posts = Post.objects.filter(title__icontains=query).filter(pub_date__lte=timezone.now())
    return render(request, 'search.html', {'posts': posts, 'search': query})


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'error_message': 'invalid login'})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
