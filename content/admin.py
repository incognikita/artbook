from django.contrib import admin
from .models import Content, UploadFile, Comment


class UploadInline(admin.TabularInline):
    model = UploadFile
    readonly_fields = ['file']
    extra = 0


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """Админка постов"""
    list_display = ['title', 'author', 'slug', 'create_post', 'publish_post', 'status']

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['status']
    raw_id_fields = ['author']
    search_fields = ['title']
    date_hierarchy = 'publish_post'
    list_editable = ['status']
    inlines = [
        UploadInline
    ]


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    """Админка изображений к постам"""
    list_display = ['content', 'file']
    search_fields = ['content']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['user', 'body']
    list_editable = ['active']
