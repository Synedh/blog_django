from django.utils import timezone

from .models import Post, Tag, Option

def posts_processor(request):
    return {'recent_posts': Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]}

def tags_processor(request):
    return {'most_used_tags': sorted(Tag.objects.all(), key=lambda x: x.post_set.count())[:5]}

def options_processor(request):
    return {'options': Option.objects.all()[0]}
