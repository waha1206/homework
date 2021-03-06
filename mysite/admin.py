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
    
#第一層的admin介面
class CategoryLevelOneAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'description')
    search_fields=('name',)
    ordering = ('name',)
    
#第二層的admin介面
class CategoryLevelTwoAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'description', 'image')
    search_fields=('name',)
    ordering = ('name',)
#第三層的admin介面
class CategoryLevelThreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'description')
    search_fields=('name',)
    ordering = ('name',)
#利潤表格
class ProfitAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields=('key',)
    ordering = ('key',)
    
class MyoSupplierAdmin(admin.ModelAdmin):
    list_display=('name', 'company_tax_id', 'tel', 'contact_sales')
    search_fields=('name',)
    ordering=('-create_time',) 
    
class MaterialLevelOneAdmin(admin.ModelAdmin):
    list_display=('create_time', 'name')
    search_fields=('name',)
    ordering=('-create_time',) 
    
class MaterialLevelTwoAdmin(admin.ModelAdmin):
    list_display=('create_time', 'name', 'category')
    search_fields=('name',)
    ordering=('-create_time',) 

class MaterialLevelThreeAdmin(admin.ModelAdmin):
    list_display=('create_time', 'name', 'category')
    search_fields=('name',)
    ordering=('-create_time',) 


admin.site.register(models.Mood)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.User2)
admin.site.register(models.Profile)
admin.site.register(models.CategoryLevelThree, CategoryLevelThreeAdmin)
admin.site.register(models.CategoryLevelTwo, CategoryLevelTwoAdmin)
admin.site.register(models.CategoryLevelOne, CategoryLevelOneAdmin)
admin.site.register(models.Profit, ProfitAdmin)
admin.site.register(models.MyoSupplier, MyoSupplierAdmin)
admin.site.register(models.MaterialLevelOne, MaterialLevelOneAdmin)
admin.site.register(models.MaterialLevelTwo, MaterialLevelTwoAdmin)
admin.site.register(models.MaterialLevelThree, MaterialLevelThreeAdmin)
