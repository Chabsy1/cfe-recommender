

from .models import Movie


def task_calculate_movie_rating_all():
    qs = Movie.objects.all()
    for obj in qs:
        obj.calculate_rating(save=True)



def task_calculate_movie_rating_needs_updating():
    qs = Movie.objects.all()
    for obj in qs:
        obj.calculate_rating(save=True)
