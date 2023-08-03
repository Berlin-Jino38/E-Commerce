from django.contrib import admin
from .models import Catagory,Product

# Register your models here.
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image','status', 'Created_at']
admin.site.register(Catagory,CatagoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'catagory', 'status', 'Trending', 'Created_at']
admin.site.register(Product,ProductAdmin)
