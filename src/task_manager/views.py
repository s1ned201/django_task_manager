from os import name

from account.models import User
from django.db.models import Prefetch, Count
from task_manager.forms import TaskForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from task_manager.models import Tasks, Comments

def tasks(request):

    context = {
        'tasks':
            Tasks.objects.
            select_related("assignee").
            prefetch_related("tags", "comments").
            all()
    }
    return render(request, 'tasks.html', context=context)

def home(request):
    return render(request, 'home.html')

# def user(request):
#
#     context = {
#         "user":
#             User.objects.all(),
#     }
#
#     return render(request, 'user_list.html', context=context)

def create_task_form(request):

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            # Tasks.objects.create(
            #     name=request.POST['name'],
            #     priority=request.POST['priority']
            # )
            form.save()
            return HttpResponseRedirect('/tasks/')
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form})


def user_list(request):
    users = User.objects.annotate(
        tasks_count=Count('tasks', distinct=True)
    )
    return render(request, 'user_list.html', {'users': users})

def user_info(request, user_id):
    user = get_object_or_404(User, id=user_id)

    tasks = Tasks.objects.filter(assignee=user).prefetch_related(
        'comments'
    )

    tasks_data = []
    total_comments = 0

    for task in tasks:
        user_comments = task.comments.filter(user=user)
        total_comments += user_comments.count()

        tasks_data.append({
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'created_at': task.created_at,
            'user_comments': user_comments,
        })

    context = {
        'user': user,
        'tasks': tasks_data,
        'total_comments': total_comments,
    }

    return render(request, 'user_info.html', context)
