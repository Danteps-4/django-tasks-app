from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("tasks")
        else:
            return render(request, "signup.html", {"form":form})
    else:
        form = UserCreationForm()
        return render(request, "signup.html", {"form":form})

def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("tasks")
            else:
                return redirect("login")
        else:
            return redirect("login")
    else:
        form = AuthenticationForm()
        return render(request, "signin.html", {"form":form})
    
def signout(request):
    logout(request)
    return redirect("home")

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, "tasks.html", {"tasks":tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=False)
    return render(request, "tasks.html", {"tasks":tasks})

@login_required
def task_detail(request, task_id):
    if request.method == "POST":
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except:
            return render(request, "task_detail.html", {"task":task, "form":form})
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    form = TaskForm(instance=task)
    return render(request, "task_detail.html", {"task":task, "form":form})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.dateCompleted = timezone.now()
        task.save()
        return redirect("tasks")

@login_required 
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")

@login_required
def create_task(request):
    if request.method == "POST":
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except:
            return render(request, "create_task.html", {"form":TaskForm})
    return render(request, "create_task.html", {"form":TaskForm})