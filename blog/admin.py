from django.contrib import admin
from blog.models import Post, Category, Comment
from django_summernote.admin import SummernoteModelAdmin



class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('title', 'author', 'created_date', 'published_date','status')
    list_filter = ('status', 'author')
    ordering = ('-published_date',)
    search_fields   = ('title', 'content',)
    summernote_fields = ('content',)


admin.site.register(Post, PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('name', 'post', 'approved', 'created_date',)
    list_filter = ('approved', 'post')
    search_fields   = ('name', 'post',)

admin.site.register(Comment, CommentAdmin)