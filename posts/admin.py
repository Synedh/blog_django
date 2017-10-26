from django.contrib import admin
from django.db.models import Count

from .models import Post, Commentary


class CommentaryInline(admin.TabularInline):
	model = Commentary
	extra = 1


class PostAdmin(admin.ModelAdmin):
	list_display = ['pub_date', 'title', 'commentary_count', 'view']
	list_filter = ['pub_date']
	search_fields =['title', 'content']
	def get_queryset(self, request):
		return Post.objects.annotate(commentary_count=Count('commentary'))

	def commentary_count(self, obj):
		return obj.commentary_count

	commentary_count.admin_order_field = 'commentary_count'

	fieldsets = [
		(None, {'fields': ['pub_date','author', 'view']}),
		('Content', {'fields': ['title', 'content']})
	]
	inlines = [CommentaryInline]

admin.site.register(Post, PostAdmin)