from django.contrib import admin
from .models import *

class CommentInlineAdmin(admin.TabularInline):# difference btw Stack and Tabular
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', )
    list_display_links = ('pk', 'title', )
    ordering = ('-id', )
    inlines = [CommentInlineAdmin]
    search_fields = ('content','title')
    list_filter = ('categories', )
    date_hierarchy = 'created_at'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Category)

