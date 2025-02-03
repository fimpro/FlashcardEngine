from django.urls import path
from .views import flashcard_view, mark_correct, flashcard_random, increment_checked,clear_all

urlpatterns = [
    path('flashcard/<int:card_id>/', flashcard_view, name='flashcard'),
    path('flashcard/<int:card_id>/correct/', mark_correct, name='mark_correct'),
path('flashcard_random/<int:range_start>/<str:hide>/', flashcard_random, name='flashcard_random'),
    path('flashcard_random/<int:range_start>/', flashcard_random, {'hide': 'none'}, name='flashcard_random_default'),
    path('flashcard_random/', flashcard_random, {'range_start': 0, 'hide': 'none'}, name='flashcard_random_home'),
path('increment_checked/<int:flashcard_id>/<str:hide>/', increment_checked, name='increment_checked'),
path('clear_all/<int:range_start>/', clear_all, name='clear_all'),
]