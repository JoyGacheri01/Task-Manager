from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from . models import Task, Category

# Create your views here.
def index(request):
    tasks = Task.objects.all().order_by('status','order', 'created_at')
    return render(request, 'index.html')

def tasks(request):
    tasks = Task.objects.all().order_by('status','order', 'created_at')
    return render(request, 'task.html' , {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status', "todo")  # New line to get status
        due_date = request.POST.get('due_date')  
        
        if not title:
            return render(request, "add_task.html", {'error': 'Title is required.'})

        Task.objects.create(title=title, description=description, due_date=due_date, status=status)
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

@require_POST
def update_task_status(request, id):
    task_id = request.POST.get('id')
    status = request.POST.get('status')
    order = request.POST.get('order')

    if not task_id or not status:
        return HttpResponseBadRequest("Missing data")
    
    task = get_object_or_404(Task, id=task_id)

    valid_statuses = [key for key, _ in Task.STATUS_CHOICES]
    if status not in valid_statuses:
        return HttpResponseBadRequest("Invalid status")
    
    task.status = status
    task.order = order
    task.save()

    return JsonResponse({'success': True, "new_status": task.get__status_display(), "new_order": task.order})