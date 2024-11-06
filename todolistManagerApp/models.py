from django.db import models
from django.contrib.auth.models import User

# Create your models here.


PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in progress', 'In Progress'),
            ('completed', 'Completed'),
        ]
    )
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    assigned_users = models.ManyToManyField(User)  # Allow multiple users

    def __str__(self):
        return self.name