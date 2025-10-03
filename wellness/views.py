from django.shortcuts import render, redirect
from .models import DailyJournal, Mood, Waterintake, GratitudeEntry

# Create your views here.

def home(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "water":
            amount = request.POST.get("amount")
            Waterintake.objects.create(amount=amount)

        elif form_type == "mood":
            mood = request.POST.get("mood")
            notes = request.POST.get("notes")
            Mood.objects.create(mood=mood, notes=notes)

        elif form_type == "gratitude":
            text = request.POST.get("text")
            GratitudeEntry.objects.create(text=text)

        elif form_type == "journal":
            entry = request.POST.get("entry")
            DailyJournal.objects.create(entry=entry)

        return redirect("home")  

    return render(request, "home.html")


def view_journal(request):
    journal_logs = DailyJournal.objects.all().order_by('-date')
    return render(request, "journal.html", {"journal_logs": journal_logs})