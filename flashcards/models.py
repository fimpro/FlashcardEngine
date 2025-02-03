from django.db import models

class Flashcard(models.Model):
    english_word = models.CharField(max_length=100)
    polish_translation = models.CharField(max_length=100)
    checked = models.IntegerField(default=0)  # New field to track correct button clicks

    def __str__(self):
        return self.english_word


