from django.db import models

# Create your models here.

class DailyJournal(models.Model):
    date = models.DateField(auto_now_add=True)
    summary = models.TextField()

    def __str__(self):
        return f"Journal Entry for {self.date}"
    
class Mood(models.Model):
    date = models.DateField(auto_now_add=True)
    mood_level = models.IntegerField()
    mood = models.CharField(max_length=50, choices=[
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('anxious', 'Anxious'),
        ('excited', 'Excited'),
    ])
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Mood on {self.date}: {self.mood}"
    
class Waterintake(models.Model):
    date = models.DateField(auto_now_add=True)
    cups = models.IntegerField()

    def __str__(self):
        return f"Water Intake on {self.date}: {self.amount_liters}L"

class GratitudeEntry(models.Model):
    date = models.DateField(auto_now_add=True)
    entry = models.TextField()

    def __str__(self):
        return f"Gratitude Entry for {self.date}"
    
