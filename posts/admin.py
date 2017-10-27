from django.contrib import admin
from django.db.models import Count

from .models import Post, Commentary, Tag


class CommentaryInline(admin.TabularInline):
    model = Commentary
    extra = 1


class PostInline(admin.TabularInline):
    model = Post.tag.through
    extra = 0


class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']
    inlines = [PostInline]


class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ['tag']
    list_display = ['pub_date', 'title', 'commentary_count', 'view']
    list_filter = ['pub_date']
    search_fields = ['title', 'content']

    def get_queryset(self, request):
        return Post.objects.annotate(commentary_count=Count('commentary'))

    def commentary_count(self, obj):
        return obj.commentary_count

    commentary_count.admin_order_field = 'commentary_count'

    fieldsets = [
        (None, {'fields': ['pub_date','author', 'view']}),
        ('Content', {'fields': ['title', 'content', 'tag']})
    ]
    inlines = [CommentaryInline]


admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)