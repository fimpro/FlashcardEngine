from django.shortcuts import render, get_object_or_404, redirect
from .models import Flashcard
from django.urls import reverse
from django.db.models import Min
import random

def flashcard_view(request, card_id=1):
    flashcards = list(Flashcard.objects.all())
    total = len(flashcards)

    if total == 0:
        return render(request, 'flashcard.html', {'card': None, 'card_id': 0, 'total': 0})

    card_id = max(1, min(card_id, total))  # Ensure card_id is within bounds
    card = flashcards[card_id - 1]

    return render(request, 'flashcard.html',
                  {'card': card, 'card_id': card_id, 'total': total, 'show_translation': False})

def flashcard_random(request, range_start=0, hide='none'):
    # Ensure range_start is a multiple of 100
    range_start = (range_start // 100) * 100
    range_end = range_start + 99

    # Get flashcards in the current range
    flashcards = Flashcard.objects.filter(id__gte=range_start, id__lte=range_end)

    # Find the minimum checked value in the range
    min_checked = flashcards.aggregate(Min('checked'))['checked__min']

    # Filter flashcards with the minimum checked value
    candidate_flashcards = flashcards.filter(checked=min_checked)

    # Select a random flashcard from the candidates
    if candidate_flashcards.exists():
        flashcard = random.choice(candidate_flashcards)
    else:
        flashcard = None

    # Determine the next and previous ranges
    next_range = range_start + 100
    prev_range = range_start - 100

    # Ensure previous range doesn't go below 0
    if prev_range < 0:
        prev_range = 0

    # Pass the context to the template
    context = {
        'flashcard': flashcard,
        'range_start': range_start,
        'next_range': next_range,
        'prev_range': prev_range,
        'hide': hide,  # 'none', 'english', or 'polish'
    }
    return render(request, 'flashcard_random.html', context)

def mark_correct(request, card_id):
    card = get_object_or_404(Flashcard, id=card_id)
    card.checked += 1
    card.save()
    return redirect('flashcard', card_id=card_id)


def increment_checked(request, flashcard_id,hide):
    print(hide)
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    flashcard.checked += 1
    flashcard.save()
    # Redirect back to the flashcard view
    return redirect(reverse('flashcard_random', args=[flashcard.id // 100 * 100, hide]))


def clear_all(request, range_start):
    # Get flashcards in the current range
    range_end = range_start + 99
    flashcards = Flashcard.objects.filter(id__gte=range_start, id__lte=range_end)

    # Reset the checked value for all flashcards in the range
    flashcards.update(checked=0)

    # Redirect back to the flashcard view for the current range
    return redirect(reverse('flashcard_random', args=[range_start, 'none']))