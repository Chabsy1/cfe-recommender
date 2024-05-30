from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ratings.models import Rating
from ratings.tasks import generate_fake_reviews

User = get_user_model()

class Command(BaseCommand):  # ability to create users
    
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?', default=10, type=int)
        parser.add_argument("--users", default=1000, type=int)
        parser.add_argument("--show-total", action='store_true', default=False)

    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        user_count = options.get('users')
        print(f"Generating {count} fake ratings for {user_count} users. Show total: {show_total}")

        try:
            print("Generating fake reviews...")
            new_ratings = generate_fake_reviews(count=count, users=user_count)
            print(f"New ratings: {len(new_ratings)}")
        except ValueError as ve:
            print(f"Value error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")

        if show_total:
            total_ratings = Rating.objects.count()
            print(f"Total ratings: {total_ratings}")
