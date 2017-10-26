from django.utils import timezone

from .models import Post

def posts_processor(request):
    return {'recent_posts': Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]}