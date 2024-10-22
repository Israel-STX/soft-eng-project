# Django imports
from django.shortcuts import render, redirect  # Consolidate render and redirect
from django.contrib.auth.decorators import login_required, user_passes_test  # Combine decorator imports
from django.contrib.auth.forms import UserChangeForm, UserCreationForm # Combine form imports
from django.contrib.auth.models import Group
from django.contrib import messages

# App-specific imports
from .forms import TaskForm, UserRegistrationForm  # Import all forms in one line
from .models import Task  # Import your Task model
from datetime import date # Imports the time for pending tasks getting close to due date


# Create your views here.
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()


@login_required
def task_list(request):
    status_filter = request.GET.get('status')
    is_admin_user = request.user.groups.filter(name='Admin').exists()

    # Fetch tasks based on user's role
    if is_admin_user:
        tasks = Task.objects.all()  # Admin sees all tasks
    else:
        tasks = Task.objects.filter(assigned_users=request.user)  # Regular users see only their tasks

    if status_filter:
        tasks = tasks.filter(status=status_filter)  # Apply status filter

    today = date.today()

    # Check for POST request to update task statuses
    if request.method == 'POST':
        for task in tasks:
            # Get the new status from the submitted form data
            new_status = request.POST.get(f'status_{task.id}')
            if new_status and task.status != new_status:
                task.status = new_status
                task.save()

        # After updating statuses, reload the task list
        return redirect('task_list')

    return render(request, 'task_list.html', {
        'tasks': tasks,
        'is_admin': is_admin_user,
        'today': today,
    })


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
def update_task_status(request):
    if request.method == 'POST':
        tasks = Task.objects.all()  # Admin can update all tasks
        # Regular users can only update their own tasks
        if not request.user.groups.filter(name='Admin').exists():
            tasks = tasks.filter(assigned_users=request.user)

        # Iterate through tasks and update their status
        for task in tasks:
            new_status = request.POST.get(f'status_{task.id}')
            if new_status and task.status != new_status:
                task.status = new_status
                task.save()

        return redirect('task_list')  # Redirect back to the task list after updates
    return redirect('task_list')  # Redirect in case of a GET request


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            # Assign the user to the correct group
            user_type = form.cleaned_data['user_type']
            if user_type == 'admin':
                admin_group = Group.objects.get(name='Admin')
                user.groups.add(admin_group)
            else:
                regular_group = Group.objects.get(name='Regular')
                user.groups.add(regular_group)

            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'There was an error with your registration. Please check the form.')
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