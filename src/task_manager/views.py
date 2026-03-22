# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from task_manager.models import Tasks

def tasks(request):

    context = {
        'tasks': Tasks.objects.all()
    }
    return render(request, 'tasks.html', context=context)

def home(request):
    return render(request, 'home.html')

def user(request):
    users = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 28},
        {"name": "Diana", "age": 22}
    ]
    context = {'users': users}

    return render(request, 'users.html', context=context)
