from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model

from cfehome import utils as cfehome_utils
User = get_user_model()

class Command(BaseCommand): #ability to create users
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?', default=10, type=int)
    def handle(self, *args, **options):
        profiles = cfehome_utils.get_fake_profiles(count=10)
