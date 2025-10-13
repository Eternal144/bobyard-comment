from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Comment
from datetime import datetime


class CommentModelTest(TestCase):
    """Test cases for Comment model"""
    
    def setUp(self):
        self.comment = Comment.objects.create(
            author="Test User",
            text="This is a test comment",
            likes=10,
            image="https://example.com/image.jpg"
        )
    
    def test_comment_creation(self):
        """Test that a comment can be created"""
        self.assertEqual(self.comment.author, "Test User")
        self.assertEqual(self.comment.text, "This is a test comment")
        self.assertEqual(self.comment.likes, 10)
        self.assertTrue(isinstance(self.comment, Comment))
    
    def test_comment_str(self):
        """Test string representation of comment"""
        self.assertIn("Test User", str(self.comment))
    
    def test_comment_default_values(self):
        """Test default values"""
        comment = Comment.objects.create(
            author="User",
            text="Test"
        )
        self.assertEqual(comment.likes, 0)
        self.assertTrue(comment.date)


class CommentAPITest(APITestCase):
    """Test cases for Comment API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.list_url = reverse('comment-list')
        
        # Create test comments
        self.comment1 = Comment.objects.create(
            author="User1",
            text="First comment",
            likes=5
        )
        self.comment2 = Comment.objects.create(
            author="User2",
            text="Second comment",
            likes=10
        )
    
    def test_get_all_comments(self):
        """Test retrieving all comments"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_single_comment(self):
        """Test retrieving a single comment"""
        url = reverse('comment-detail', kwargs={'pk': self.comment1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], "First comment")
    
    def test_create_comment(self):
        """Test creating a new comment"""
        data = {
            'author': 'Admin',
            'text': 'New test comment',
            'likes': 0
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 3)
        self.assertEqual(response.data['author'], 'Admin')
    
    def test_create_comment_without_author(self):
        """Test creating comment defaults to Admin"""
        data = {
            'text': 'Comment without author'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], 'Admin')
    
    def test_create_comment_empty_text(self):
        """Test that empty text fails validation"""
        data = {
            'author': 'User',
            'text': ''
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_comment(self):
        """Test updating a comment"""
        url = reverse('comment-detail', kwargs={'pk': self.comment1.pk})
        data = {
            'author': 'User1',
            'text': 'Updated comment text',
            'likes': 15
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.text, 'Updated comment text')
    
    def test_partial_update_comment(self):
        """Test partial update (PATCH)"""
        url = reverse('comment-detail', kwargs={'pk': self.comment1.pk})
        data = {'text': 'Partially updated'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.text, 'Partially updated')
        self.assertEqual(self.comment1.author, 'User1')  # Should remain unchanged
    
    def test_delete_comment(self):
        """Test deleting a comment"""
        url = reverse('comment-detail', kwargs={'pk': self.comment1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)
    
    def test_delete_nonexistent_comment(self):
        """Test deleting a comment that doesn't exist"""
        url = reverse('comment-detail', kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_comment_ordering(self):
        """Test that comments are ordered by date (newest first)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The second comment should appear first (created later)
        self.assertEqual(response.data[0]['text'], 'Second comment')
