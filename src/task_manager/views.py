from os import name

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.template.defaultfilters import filesizeformat
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from account.models import User
from django.db.models import Prefetch, Count, Q
from task_manager.forms import TaskForm, CommentForm, UserCreateForm, AttachmentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from task_manager.models import Tasks, Comments, Attachments
from task_manager.models.tasks import TaskStatus




#TASK
# def tasks(request):
#     tasks = Tasks.objects.task_optimization()
#     paginator = Paginator(tasks, 10)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         'tasks': page_obj,
#         'page_obj': page_obj,
#         'paginator': paginator,
#     }
#     return render(request, 'tasks.html', context=context)

# @cache_page(60*30)
class TaskView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'tasks.html'
    permission_required = 'task_manager.view_task'
    login_url = '/admin/login'
    model = Tasks
    paginate_by = 10
    paginator_class = Paginator
    queryset = Tasks.objects.task_optimization()
    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        page_number = self.request.GET.get(self.page_kwarg)
        paginator = self.paginator_class(self.queryset, self.paginate_by)
        context['tasks'] = paginator.get_page(page_number)
        context['page_obj'] = paginator.get_page(page_number)
        return context



class TaskDetailView(DetailView):
    template_name = 'task_detail.html'
    model = Tasks
    context_object_name = 'task'
    queryset = Tasks.objects.task_detail_qs()
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        task = self.get_object()
        comments = task.comments.all().order_by('-created_at')
        context['comments'] = comments
        context['comment_count'] = comments.count()
        return context


class TaskCreateView(CreateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        task = form.save()
        cache.clear()
        from django.contrib import messages
        messages.success(self.request, f'Задача "{task.name}" успешно создана!')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



# def create_task_form(request):
#
#     if request.method == "POST":
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save()
#             cache.clear()
#             return redirect('/tasks/', task_id=task.id)
#     else:
#         form = TaskForm()
#
#     return render(request, 'task_form.html', {'form': form}, )

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


#USERS

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


#ATTACHEMENT

def create_attachment(request):
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            attachment = form.save()
            messages.success(
                request,
                f'Вложение "{attachment.name}" успешно загружено!'
            )
            return redirect('attachment_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

    else:
        form = AttachmentForm()

    return render(request, 'attachment_form.html', {'form': form})


def attachment_list(request):
    task_filter = request.GET.get('task', '')
    attachments = Attachments.objects.select_related('task').all()
    if task_filter and task_filter != 'all':
        attachments = attachments.filter(task_id=task_filter)
    paginator = Paginator(attachments, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    tasks = Tasks.objects.all()
    for attachment in page_obj:
        attachment.preview = get_attachment_preview(attachment)
    context = {
        'page_obj': page_obj,
        'tasks': tasks,
        'selected_task': task_filter,
        'total_count': attachments.count(),
    }

    return render(request, 'attachment_list.html', context)


def get_attachment_preview(attachment):
    if attachment.is_image():
        return mark_safe(
            f'<img src="{attachment.file.url}" style="max-width: 100px; max-height: 100px; border-radius: 8px;" alt="{attachment.name}">'
        )
    else:
        icons = {
            'pdf': 'bi-file-earmark-pdf',
            'word': 'bi-file-earmark-word',
            'text': 'bi-file-earmark-text',
            'file': 'bi-file-earmark',
        }
        icon = icons.get(attachment.get_file_type(), 'bi-file-earmark')
        return mark_safe(
            f'<i class="bi {icon}" style="font-size: 3rem; color: #6c757d;"></i>'
            f'<div class="small text-muted mt-1">{attachment.file_size | filesizeformat}</div>'
        )


def delete_attachment(request, attachment_id):
    attachment = get_object_or_404(Attachments, id=attachment_id)
    task_id = attachment.task.id
    attachment_name = attachment.name
    attachment.delete()

    messages.success(
        request,
        f'Вложение "{attachment_name}" успешно удалено!'
    )
    return redirect('attachment_list')


def download_attachment(request, attachment_id):

    attachment = get_object_or_404(Attachments, id=attachment_id)

    if attachment.file:
        return redirect(attachment.file.url)

    messages.error(request, 'Файл не найден.')
    return redirect('attachment_list')






def home(request):
    total_tasks = Tasks.objects.count()
    completed_tasks = Tasks.objects.filter(status=TaskStatus.COMPLETED).count()
    in_progress_tasks = Tasks.objects.filter(status=TaskStatus.STARTED).count()
    total_users = User.objects.count()
    completion_percentage = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0)
    recent_tasks = Tasks.objects.all().order_by('-created_at')[:5]
    status_counts = Tasks.objects.values('status').annotate(count=Count('id'))
    total = sum(item['count'] for item in status_counts)

    status_display = {
        TaskStatus.CREATED: 'Создана',
        TaskStatus.STARTED: 'Запущена',
        TaskStatus.COMPLETED: 'Завершена',
        TaskStatus.CANCELED: 'Отменена',
        TaskStatus.FAILED: 'Провалена',
    }

    for item in status_counts:
        item['percentage'] = round((item['count'] / total * 100) if total > 0 else 0)
        item['status_display'] = status_display.get(item['status'], item['status'])

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'total_users': total_users,
        'completion_percentage': completion_percentage,
        'recent_tasks': recent_tasks,
        'status_counts': status_counts,
    }

    return render(request, 'home.html', context)

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