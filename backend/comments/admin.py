from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for Comment model
    """
    list_display = ['id', 'author', 'truncated_text', 'date', 'likes', 'has_image']
    list_filter = ['author', 'date']
    search_fields = ['author', 'text']
    ordering = ['-date']
    readonly_fields = ['date']
    
    def truncated_text(self, obj):
        """Display truncated comment text"""
        return obj.text[:75] + '...' if len(obj.text) > 75 else obj.text
    truncated_text.short_description = 'Text'
    
    def has_image(self, obj):
        """Display whether comment has an image"""
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Image'
