from django.contrib import admin
# from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
admin.site.register(Comment)

class CategoryAdmin(admin.ModelAdmin) :
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin) :
    prepopulated_fields = {'slug' : ('name',)}

class PostAdmin(SummernoteModelAdmin) :
    summernote_fields = ('content',)

admin.site.register(Post, SummernoteModelAdmin)
admin.site.register(Tag, TagAdmin)


