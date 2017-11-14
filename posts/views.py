import requests

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone

from .models import Post, Commentary, Option


def pagination(posts, page):
    try:
        post_per_page = Option.objects.filter(used=True)[0].nb_post_page
        if post_per_page > len(posts) or post_per_page == 0:
            post_per_page = len(posts)
    except IndexError:
        post_per_page = 5

    if (page < 0) or (page * post_per_page - 4 > len(posts)) :
        raise Http404("Page not found")

    # replace numbers by '...' if there is more than 3 pages before or after current page
    pages = [i for i in range(1, int((len(posts) - 1) / post_per_page) + 2)]
    posts = posts[(page - 1) * post_per_page:(page - 1) * post_per_page + post_per_page]
    pages = ((pages[0:page - 1] if len(pages[0:page - 1]) < 4 else [pages[0], '...', pages[page - 2]])
            + [pages[page - 1]] 
            + (pages[page:] if len(pages[page:]) < 4 else [pages[page], '...', pages[-1]]))
    return {
        'posts':posts, 
        'pages': pages,
        'current_page': page
    }


def index(request, page=1):
    posts = Post.objects.filter(pub_date__lte=timezone.now()).filter(show_post=True).order_by('-pub_date')
    options = pagination(posts, int(page))
    options['current'] = 'index'
    return render(request, 'index.html', options)

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
    if not commentary.validated:
        raise Http404("Page not found")
    return render(request, 'commentary_wrapper.html', {'commentary': commentary})


def search(request, page=1):
    query = request.POST['search']
    posts = Post.objects.filter(pub_date__lte=timezone.now()).filter(title__icontains=query).order_by('-pub_date')
    if len(posts) == 0:
        return render(request, 'index.html', {'search': query, 'current': 'search'})
    options = pagination(posts, int(page) if page else 1)
    options['search'] = query
    options['current'] = 'search'
    return render(request, 'index.html', options)


def posts_by_author(request, author, page=1):
    posts = Post.objects.filter(pub_date__lte=timezone.now()).filter(author__iexact=author).order_by('-pub_date')
    return render(request, 'index.html', {'posts': posts})


def posts_by_tag(request, tags):
    tags = tags.split('/')
    posts = Post.objects.filter(pub_date__lte=timezone.now()).filter(tag__tag__in=tags).order_by('-pub_date')
    return render(request, 'index.html', {'posts': posts})


def login(request):
    user = authenticate(
        request,
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is not None:
        auth_login(request, user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'error_message': 'invalid login'})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
