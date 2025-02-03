import csv
from flashcards.models import Flashcard

def import_flashcards(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) == 2:
                english, polish = row
                Flashcard.objects.get_or_create(english_word=english, polish_translation=polish)
    print("Flashcards imported successfully!")