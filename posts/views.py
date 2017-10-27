import requests

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone

from .models import Post, Commentary


def index(request, page=1):
    page = int(page)
    posts = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    if (page == 0) or (page * 5 - 4 > len(posts)) :
        raise Http404("Page not found")
    pages = [i for i in range(1, int((len(posts) - 1) / 5) + 2)]
    posts = posts[(page - 1) * 5:(page - 1) * 5 + 5]
    # Pagination
    # replace numbers by '...' if there is more than 3 pages before or after current page
    pages = ((pages[0:page - 1] if len(pages[0:page - 1]) < 4 else [pages[0], '...', pages[page - 2]])
            + [pages[page - 1]] 
            + (pages[page:] if len(pages[page:]) < 4 else [pages[page], '...', pages[-1]]))
    return render(request, 'index.html', {'posts': posts,
                                          'pages': pages,
                                          'current_page': page})

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.pub_date > timezone.now():
        raise Http404("Page not found")
    if 'post_view' not in request.session.keys():
        request.session['post_view'] = []
    if post_id not in request.session['post_view']:
        post.view += 1
        post.save()
        request.session['post_view'] += post_id
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
    posts = Post.objects.filter(pub_date__lte=timezone.now()).filter(title__icontains=query).order_by('-pub_date')
    return render(request, 'index.html', {'posts': posts, 'search': query})


def posts_by_author(request, author):
    posts = Post.objects.filter(pub_date__lte=timezone.now()).filter(author__iexact=author).order_by('-pub_date')
    return render(request, 'index.html', {'posts': posts})


def posts_by_tag(request, tags):
    posts = Post.objects.filter(pub_date__lte=timezone.now()).fitler().order_by('-pub_date')
    return render(request, 'index.html', {'posts': posts})


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
