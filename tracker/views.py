from django.shortcuts import render, redirect
from . models import Task
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'tasks.html' , {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')  # New line to get due_date

        Task.objects.create(title=title, description=description, due_date=due_date)
        return redirect('tasks')
    return render(request, "add_task.html")

def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('/')

def update_task(request, id):
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')  # New line to update due_date

        task.save()
        return redirect('tasks')
    return render(request, 'update_task.html', {'task': task})

def search_tasks(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Task.objects.filter(
            Q(title_icontains=query) | Q(description_icontains = query)
        )

    return render(request, 'search.html', {'results': results, 'query': query})