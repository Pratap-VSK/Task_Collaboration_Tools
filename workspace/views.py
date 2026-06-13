from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Project, Task, Comment
from django.contrib.auth.models import User
import json
from accounts.models import UserProfile 


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'workspace/home.html')

@login_required
def dashboard(request):
    user = request.user
    
    # Ye line magic karegi: agar profile nahi hai toh automatically bana degi
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    projects = Project.objects.filter(Q(owner=user) | Q(members=user)).distinct()
    total_tasks = Task.objects.filter(project__in=projects).count()
    assigned_tasks = Task.objects.filter(assigned_to=user).exclude(status='done')
    recent_tasks = Task.objects.filter(project__in=projects).order_by('-created_at')[:5]

    context = {
        'user_profile': user_profile, # Isko context mein pass kar do
        'projects': projects,
        'total_tasks': total_tasks,
        'assigned_tasks': assigned_tasks.count(),
        'recent_tasks': recent_tasks,
    }
    return render(request, 'workspace/dashboard.html', context)

@login_required
def project_list(request):
    user = request.user
    projects = Project.objects.filter(Q(owner=user) | Q(members=user)).distinct()
    return render(request, 'workspace/project_list.html', {'projects': projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user not in [project.owner] + list(project.members.all()):
        return redirect('dashboard')

    view_type = request.GET.get('view', 'kanban')
    tasks = project.tasks.all()

    if request.GET.get('status'):
        tasks = tasks.filter(status=request.GET.get('status'))
    if request.GET.get('priority'):
        tasks = tasks.filter(priority=request.GET.get('priority'))

    context = {
        'project': project,
        'tasks': tasks,
        'view_type': view_type,
        'statuses': dict(Task.STATUS_CHOICES),
        'priorities': dict(Task.PRIORITY_CHOICES),
    }
    return render(request, 'workspace/project_detail.html', context)


@login_required
def project_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        color = request.POST.get('color', '#3B82F6')

        project = Project.objects.create(
            name=name,
            description=description,
            owner=request.user,
            color=color
        )
        project.members.add(request.user)
        return redirect('project_detail', pk=project.pk)

    return render(request, 'workspace/project_form.html')


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        project.name = request.POST.get('name')
        project.description = request.POST.get('description')
        project.color = request.POST.get('color')
        project.save()
        return redirect('project_detail', pk=project.pk)

    context = {'project': project, 'is_edit': True}
    return render(request, 'workspace/project_form.html', context)


@login_required
def project_members(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            project.members.add(user)
        except:
            massages.error(request, 'User Not Found')
        return redirect('project_members', pk=project.pk)

    context = {'project': project}
    return render(request, 'workspace/project_members.html', context)


@login_required
def project_delete_member(request, pk, member_id):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        return redirect('dashboard')

    member = get_object_or_404(User, pk=member_id)
    project.members.remove(member)
    return redirect('project_members', pk=project.pk)
    t.method == 'POST':

    title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date') or None
        assigned_to_id = request.POST.get('assigned_to')

@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    # ... baki ka code waisa hi rahega ...

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date') or None
        assigned_to_id = request.POST.get('assigned_to')

        assigned_to = None
        if assigned_to_id:
            assigned_to = get_object_or_404(User, pk=assigned_to_id)

        # YAHAN STATUS ADD KAREIN ('todo' ya jo bhi aapki models.py mein To Do ki key hai)
        Task.objects.create(
            title=title,
            description=description,
            project=project,
            created_by=request.user,
            priority=priority,
            status='todo',  # <--- YEH LINE ADD KARNI HAI
            due_date=due_date,
            assigned_to=assigned_to
        )
return redirect('project_detail', pk=project.pk)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    if request.user not in [project.owner] + list(project.members.all()):
        return redirect('dashboard')

    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.priority = request.POST.get('priority', task.priority)
        task.status = request.POST.get('status', task.status)
        task.due_date = request.POST.get('due_date') or task.due_date

        assigned_to_id = request.POST.get('assigned_to')
        if assigned_to_id:
            task.assigned_to = get_object_or_404(User, pk=assigned_to_id)
        task.save()
        return redirect('task_detail', pk=task.pk)

    comments = task.comments.all()
    context = {
        'task': task,
        'comments': comments,
        'statuses': dict(Task.STATUS_CHOICES),
        'priorities': dict(Task.PRIORITY_CHOICES),
        'members': task.project.members.all()
    }
    return render(request, 'workspace/task_detail.html', context)


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk

    if request.user != task.created_by and task.project.owner != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', pk=project_pk)

    context = {'task': task}
    return render(request, 'workspace/task_confirm_delete.html', context)


@login_required
@require_http_methods(["POST"])
def add_comment(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    project = task.project
    if request.user not in [project.owner] + list(project.members.all()):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    content = request.POST.get('content')
    comment = Comment.objects.create(
        task=task,
        author=request.user,
        content=content
    )

    return JsonResponse({
        'id': comment.id,
        'author': comment.author.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })


@login_required
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    task = comment.task
    project = task.project

    if request.user != comment.author and project.owner != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        comment.delete()
        return redirect('task_detail', pk=task.pk)

    context = {'comment': comment, 'task': task}
    return render(request, 'workspace/comment_confirm_delete.html', context)


@login_required
@require_http_methods(["POST"])
def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    if request.user not in [project.owner] + list(project.members.all()):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        data = json.loads(request.body)
        task.status = data.get('status', task.status)
        task.order = data.get('order', task.order)
        task.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def my_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user).exclude(status='done')
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    context = {
        'tasks': tasks,
        'statuses': dict(Task.STATUS_CHOICES),
    }
    return render(request, 'workspace/my_tasks.html', context)


def terms_of_service(request):
    return render(request, 'legal/terms_of_service.html')


def privacy_policy(request):
    return render(request, 'legal/privacy_policy.html')


def contact_us(request):
    return render(request, 'legal/contact_us.html')


def about_us(request):
    return render(request, 'legal/about_us.html')


def blog(request):
    return render(request, 'legal/blog.html')
