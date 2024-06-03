from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.db.models import Avg
from ratings.models import Movie
import decimal

class Command(BaseCommand):
    help = 'Update movie ratings in batches'

    def handle(self, *args, **kwargs):
        self.update_all_movie_ratings()

    def update_all_movie_ratings(self):
        movie_ids = list(Movie.objects.values_list('id', flat=True))
        batch_size = 100
        for i in range(0, len(movie_ids), batch_size):
            batch_ids = movie_ids[i:i + batch_size]
            self.update_movie_ratings_batch(batch_ids)

    @transaction.atomic
    def update_movie_ratings_batch(self, movie_ids):
        for movie_id in movie_ids:
            qs = Movie.objects.filter(id=movie_id)
            if qs.exists():
                movie = qs.first()
                rating_avg = movie.rating_set.aggregate(Avg('rating'))['rating__avg']
                rating_count = movie.rating_set.count()
                score = decimal.Decimal(rating_avg * rating_count * 1.0)
                qs.update(
                    rating_avg=rating_avg,
                    rating_count=rating_count,
                    score=score,
                    rating_last_updated=timezone.now()
                )
