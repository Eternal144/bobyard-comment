import json
import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from comments.models import Comment


class Command(BaseCommand):
    help = 'Load comments from JSON file'

    def add_arguments(self, parser):
        # Default path: backend/data/comments.json
        default_path = os.path.join(settings.BASE_DIR, 'data', 'comments.json')
        parser.add_argument(
            '--file',
            type=str,
            default=default_path,
            help='Path to the JSON file containing comments'
        )

    def handle(self, *args, **options):
        json_file = options['file']
        
        # If relative path, resolve it relative to BASE_DIR
        if not os.path.isabs(json_file):
            json_file = os.path.join(settings.BASE_DIR, json_file)
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            # If the JSON has a "comments" key, extract it
            if isinstance(data, dict) and 'comments' in data:
                comments_data = data['comments']
            elif isinstance(data, list):
                comments_data = data
            else:
                raise ValueError('Invalid JSON structure. Expected a list or dict with "comments" key.')
            
            # Clear existing data (optional)
            Comment.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing comments'))
            
            # Import new data
            created_count = 0
            for comment_data in comments_data:
                Comment.objects.create(
                    author=comment_data.get('author', 'Anonymous'),
                    text=comment_data.get('text', ''),
                    date=comment_data.get('date', timezone.now()),
                    likes=comment_data.get('likes', 0),
                    image=comment_data.get('image', '') or ''  # Handle None values
                )
                created_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded {created_count} comments from {json_file}')
            )
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {json_file}')
            )
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON format: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
