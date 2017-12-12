from django.contrib import admin

from .models import Category, Post, Tag
from .forms import BlogPostForm

class PostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    list_display = ['title', 'created_time', 'pub_date', 'modified_time', 'category', 'author',
                    'views', 'status'
                    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
