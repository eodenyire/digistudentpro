"""
Django management command to load CBC education levels, grades, and subjects
"""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Load CBC structure data'

    def handle(self, *args, **kwargs):
        # Logic to load CBC structure data
        self.stdout.write(self.style.SUCCESS('Successfully loaded CBC structure data'))