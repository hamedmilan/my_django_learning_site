from django.contrib import admin
from blog.models import Post, Category



class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('title', 'author', 'created_date', 'published_date','status')
    list_filter = ('status', 'author')
    ordering = ('-published_date',)
    search_fields   = ('title', 'content',)


admin.site.register(Post, PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
