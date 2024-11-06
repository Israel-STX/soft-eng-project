from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Display key fields in the task list view
    list_display = ('name', 'due_date', 'status', 'priority', 'display_assigned_users')
    
    # Allow filtering based on status, priority, and due_date
    list_filter = ('status', 'priority', 'due_date')
    
    # Enable search functionality for task names and descriptions
    search_fields = ('name', 'description')
    
    # Editable fields directly in the list view (optional)
    list_editable = ('status', 'priority')
    
    # Add a date hierarchy for easier navigation based on due_date
    date_hierarchy = 'due_date'
    
    # Fields to display when editing/creating a task
    fields = ('name', 'description', 'due_date', 'status', 'priority', 'assigned_users')
    
    # Allow inline editing for assigned users
    filter_horizontal = ('assigned_users',)

    # Customize how assigned users are displayed in the list view
    def display_assigned_users(self, obj):
        return ", ".join([user.username for user in obj.assigned_users.all()])
    
    display_assigned_users.short_description = 'Assigned Users'

