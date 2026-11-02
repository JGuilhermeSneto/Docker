from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from .models import Task
from .utils import get_system_info

def index(request):
    """Main dashboard displaying tasks, system diagnostics, and metrics."""
    status_filter = request.GET.get('status', 'all')
    category_filter = request.GET.get('category', 'all')
    
    tasks_qs = Task.objects.all()
    
    if status_filter != 'all':
        tasks_qs = tasks_qs.filter(status=status_filter)
    if category_filter != 'all':
        tasks_qs = tasks_qs.filter(category=category_filter)
        
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status='pending').count()
    in_progress_tasks = Task.objects.filter(status='in_progress').count()
    completed_tasks = Task.objects.filter(status='completed').count()
    
    context = {
        'tasks': tasks_qs,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'category_choices': Task.CATEGORY_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
        'status_choices': Task.STATUS_CHOICES,
    }
    return render(request, 'cloudtasks/index.html', context)

@require_POST
def task_create(request):
    """Create a new task."""
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    category = request.POST.get('category', 'docker')
    priority = request.POST.get('priority', 'medium')
    status = request.POST.get('status', 'pending')

    if not title:
        messages.error(request, 'O título da tarefa é obrigatório.')
        return redirect('index')

    Task.objects.create(
        title=title,
        description=description,
        category=category,
        priority=priority,
        status=status,
    )
    messages.success(request, f'Tarefa "{title}" criada com sucesso!')
    return redirect('index')

@require_POST
def task_update_status(request, task_id):
    """Update task status (pending -> in_progress -> completed)."""
    task = get_object_or_404(Task, id=task_id)
    new_status = request.POST.get('status')
    
    if new_status in dict(Task.STATUS_CHOICES):
        task.status = new_status
        task.save()
        messages.success(request, f'Status de "{task.title}" atualizado para {task.get_status_display()}!')
    return redirect('index')

@require_POST
def task_delete(request, task_id):
    """Delete a task."""
    task = get_object_or_404(Task, id=task_id)
    title = task.title
    task.delete()
    messages.info(request, f'Tarefa "{title}" removida com sucesso.')
    return redirect('index')

def theory_view(request):
    """Dedicated page with Docker & Cloud theory for the professor."""
    return render(request, 'cloudtasks/theory.html')

# REST API endpoints
@require_GET
def api_system_info(request):
    """Returns JSON payload with container & system diagnostics."""
    return JsonResponse(get_system_info())

@require_GET
def api_tasks(request):
    """Returns all tasks in JSON format."""
    tasks = list(Task.objects.values('id', 'title', 'description', 'category', 'priority', 'status', 'created_at'))
    return JsonResponse({'count': len(tasks), 'tasks': tasks})
