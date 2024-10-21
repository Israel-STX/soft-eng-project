# Django imports
from django.shortcuts import render, redirect  # Consolidate render and redirect
from django.contrib.auth.decorators import login_required, user_passes_test  # Combine decorator imports
from django.contrib.auth.forms import UserChangeForm # Combine form imports
from django.contrib.auth.models import Group

# App-specific imports
from .forms import TaskForm, UserRegistrationForm  # Import all forms in one line
from .models import Task  # Import your Task model


# Create your views here.
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()


@login_required
def task_list(request):
    status_filter = request.GET.get('status')
    is_admin_user = is_admin(request.user)  # Use the function here to check if the user is an admin

    if is_admin_user:
        tasks = Task.objects.all()  # Admin sees all tasks
    else:
        tasks = Task.objects.filter(assigned_user=request.user)  # Regular users see only their tasks

    if status_filter:
        tasks = tasks.filter(status=status_filter)  # Apply status filter

    return render(request, 'task_list.html', {'tasks': tasks, 'is_admin': is_admin})


@login_required
@user_passes_test(is_admin)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


@login_required
def update_task_status(request, task_id):
    task = Task.objects.get(id=task_id, assigned_user=request.user)
    if request.method == 'POST':
        task.status = request.POST['status']
        task.save()
        return redirect('task_list')
    return render(request, 'update_task_status.html', {'task': task})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})