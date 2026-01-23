"""
Django management command to load KUCCPS career data
"""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Load KUCCPS career data'

    def handle(self, *args, **kwargs):
        # Logic to load KUCCPS career data
        self.stdout.write(self.style.SUCCESS('Successfully loaded KUCCPS career data'))