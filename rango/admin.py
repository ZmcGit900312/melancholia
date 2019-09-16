from django.contrib import admin
from rango.models import Category,Page,UserProfile


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','views','likes','slug')
    prepopulated_fields = dict(slug=('name',))

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','views','category','url')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile)