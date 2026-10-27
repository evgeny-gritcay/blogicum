from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.text import Truncator

from .constants import TEXT_LENGTH
from .models import Category, Comment, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'post_image_thumb',
        'title',
        'is_published',
        'category',
    )
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'text')
    save_on_top = True

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'category', 'text'),
        }),
        ('Медиа', {
            'fields': ('image',),
            'classes': ('collapse',),
        }),
        ('Публикация', {
            'fields': ('is_published', 'pub_date'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('pub_date',)

    @admin.display(description='Фото')
    def post_image_thumb(self, obj: Post) -> str:
        if obj.image and obj.image.url:
            img_style = 'object-fit:cover; border-radius:4px;'
            return mark_safe(
                f'<img src="{obj.image.url}" width="60" height="60" '
                f'style="{img_style}">'
            )
        return '—'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published'
    )
    list_editable = (
        'is_published',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published'
    )
    list_editable = (
        'is_published',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post',
        'author',
        'text_preview',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    list_filter = ('is_published', 'post', 'created_at')
    search_fields = ('text', 'author__username', 'post__title')

    @admin.display(description='Пост')
    def post_title(self, obj):
        return obj.post.title if obj.post else "—"

    @admin.display(description='Текст (превью)')
    def text_preview(self, obj: Comment) -> str:
        if not obj.text:
            return '—'
        return Truncator(obj.text).chars(TEXT_LENGTH)
