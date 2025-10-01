from django.shortcuts import render, redirect
from . models import Task
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tasks(request):
    students = Task.objects.all()
    return render(request, 'tasks.html')

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Task.objects.create(title=title, description=description)
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