from django.contrib import admin
from website.models import Contact, Newsletter



class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_date',)
    list_filter = ('email',)


admin.site.register(Contact, ContactAdmin)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email',)

admin.site.register(Newsletter, NewsletterAdmin)