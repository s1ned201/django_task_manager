from os import name

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.urls import reverse

from account.models import User
from django.db.models import Prefetch, Count
from task_manager.forms import TaskForm, CommentForm, UserCreateForm, AttachmentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from task_manager.models import Tasks, Comments


def tasks(request):
    tasks = Tasks.objects.select_related("assignee").prefetch_related("tags", "comments").all()
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'tasks': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'tasks.html', context=context)
def task_detail(request, task_id):
    task = get_object_or_404(Tasks.objects.prefetch_related('tags', 'comments__user', 'attachments'), id=task_id)
    comments = task.comments.all().order_by('-created_at')

    context = {
        'task': task,
        'comments': comments,
        'comment_count': comments.count(),
    }

    return render(request, 'task_detail.html', context)

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

def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f'Пользователь "{user.username}" успешно создан!'
            )
            return redirect('user_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserCreateForm()

    return render(request, 'user_create.html', {
        'form': form,
        'title': 'Создание пользователя',
        'button_text': 'Создать'
    })

def create_task_form(request):

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('/tasks/', task_id=task.id)
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form}, )

def edit_task_form(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Задача "{task.name}" успешно обновлена!')
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_edit.html', {
        'form': form,
        'task': task
    })


def add_comment(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comments.objects.create(
                task=task,
                message=form.cleaned_data['message'],
                user=form.cleaned_data['user']
            )
            messages.success(request, 'Комментарий добавлен!')
            return redirect('tasks')
    else:
        form = CommentForm()

    return render(request, 'comment_form.html', {
        'form': form,
        'task': task
    })


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

def create_attachment(request):
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks'))

    else:
        form = AttachmentForm()

    return render(request, 'task_attachment.html', {'form': form})