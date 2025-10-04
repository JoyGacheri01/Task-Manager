from django.shortcuts import render, redirect
from .models import DailyJournal, Mood, Waterintake, GratitudeEntry

# Create your views here.

def home(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "water":
            amount = request.POST.get("amount")
            Waterintake.objects.create(cups=amount)

        elif form_type == "mood":
            mood = request.POST.get("mood")
            notes = request.POST.get("notes")
            Mood.objects.create(mood=mood, notes=notes)

        elif form_type == "gratitude":
            entry = request.POST.get("entry")
            GratitudeEntry.objects.create(entry=entry)

        elif form_type == "journal":
            summary = request.POST.get("summary")
            DailyJournal.objects.create(summary=summary)

        return redirect("home")  

    return render(request, "home.html")


def view_journal(request):
    gratitude = GratitudeEntry.objects.all().order_by('-date')
    journal = DailyJournal.objects.all().order_by('-date')
    return render(request, "journal.html", {"journal": journal, 'gratitude':gratitude})

