from django.contrib import admin
from .models import Practica,Post


@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")  
    search_fields = ("username",)                  
    list_filter = ("username",)                    

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "post_type", "author", "created_at")
    search_fields = ("title", "genre", "tags")
    list_filter = ("post_type", "genre", "created_at")