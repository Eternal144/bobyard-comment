from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model with validation
    """
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'date', 'likes', 'image']
        read_only_fields = ['id', 'date']
    
    def validate_text(self, value):
        """
        Validate that comment text is not empty
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Comment text cannot be empty")
        return value.strip()
    
    def validate_author(self, value):
        """
        Validate author name
        """
        if value and len(value.strip()) > 100:
            raise serializers.ValidationError("Author name is too long (max 100 characters)")
        return value.strip() if value else "Admin"
    
    def validate_likes(self, value):
        """
        Validate likes count is non-negative
        """
        if value < 0:
            raise serializers.ValidationError("Likes count cannot be negative")
        return value
    
    def validate_image(self, value):
        """
        Validate image URL if provided
        """
        if value and len(value) > 500:
            raise serializers.ValidationError("Image URL is too long (max 500 characters)")
        return value
