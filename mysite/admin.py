from django.contrib import admin
from mysite import models

# Register your models here.
admin.site.register(models.Maker)
admin.site.register(models.PModel)
admin.site.register(models.PPhoto)

# admin.site.register(models.Product)

class ProductAdmin(admin.ModelAdmin):
    list_display=('pmodel', 'nickname', 'price', 'year')
    search_fields=('nickname',)
    ordering=('-price',) 
    
admin.site.register(models.Product, ProductAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'message', 'enabled', 'pub_time')
    ordering = ('-pub_time',)

admin.site.register(models.Mood)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.User2)
admin.site.register(models.Profile)