from django.contrib import admin
from django.db.models import Count

from .models import Post, Commentary, Tag, Option


class CommentaryInline(admin.TabularInline):
    model = Commentary
    extra = 1


class PostInline(admin.TabularInline):
    model = Post.tag.through
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']
    list_display = ['tag', 'post_count']
    inlines = [PostInline]

    def post_count(self, obj):
        return obj.post_set.count()


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    search_fields = ['post', 'author']
    list_filter = ['pub_date', 'validated']
    list_display = ['pub_date', 'post', 'author', 'validated']

    def validate_all(self, request, queryset):
        queryset.update(validated=True)

    def unvalidate_all(self, request, queryset):
        queryset.update(validated=False)
    validate_all.short_description = "Validate"
    unvalidate_all.short_description = "Unvalidate"

    actions = [validate_all, unvalidate_all]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ['tag']
    list_display = ['pub_date', 'title', 'commentary_count', 'view', 'show_post']
    list_filter = ['pub_date']
    search_fields = ['title', 'content']

    def get_queryset(self, request):
        return Post.objects.annotate(commentary_count=Count('commentary'))

    def commentary_count(self, obj):
        return obj.commentary_count

    commentary_count.admin_order_field = 'commentary_count'

    fieldsets = [
        (None, {'fields': ['pub_date','author', 'view', 'show_post', 'allow_comments']}),
        ('Content', {'fields': ['title', 'content', 'tag']})
    ]
    inlines = [CommentaryInline]

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['nb_post_page', 'message', 'recent_posts', 'most_used_tags']
    fieldsets = [
        (None, {'fields': ['nb_post_page', 'message', 'recent_posts', 'most_used_tags']})
    ]
