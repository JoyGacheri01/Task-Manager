from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from . models import Task, Category

# Create your views here.
def index(request):
    tasks = Task.objects.all().order_by('status','order', 'created_at')

    today = timezone.now().date()
    tasks_today = Task.objects.filter(due_date=today)
    tasks_pending = Task.objects.filter(status='pending')
    tasks_in_progress= Task.objects.filter(status='in_progress')
    tasks_completed = Task.objects.filter(status='completed')

    upcoming_tasks = Task.objects.filter(
        due_date__gte=today
    ).exclude(status='completed').order_by('due_date')[:5]

    context = {
        'tasks':tasks,
        'tasks_today': tasks_today,
        'tasks_pending':tasks_pending,
        'tasks_in_progress':tasks_in_progress,
        'tasks_completed':tasks_completed,
        'upcoming_tasks': upcoming_tasks
    }
    return render(request, 'index.html', context)

def tasks(request):
    tasks = Task.objects.all().order_by('status','order', 'created_at')
    return render(request, 'task.html' , {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status', "pending")  # New line to get status
        due_date_str = request.POST.get('due_date')  
        due_date = None

        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        if not title:
            return render(request, "add_task.html", {'error': 'Title is required.'})

        Task.objects.create(title=title, due_date=due_date, status=status)
        return redirect('/')
    return render(request, "add_task.html")

def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('/')

def update_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status', "pending")  # New line to get status
        due_date_str = request.POST.get('due_date')  
        due_date = None

        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        task.save()

        Task.objects.create(title=title, due_date=due_date, status=status)

        return redirect('tasks')
    return render(request, 'update_task.html', {'task': task, })

def search_tasks(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
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

    return JsonResponse({'success': True, "new_status": task.get_status_display(), "new_order": task.order})

