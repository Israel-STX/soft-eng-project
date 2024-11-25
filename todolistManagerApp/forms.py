from django import forms
from .models import Task
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList


class SingleError(ErrorList):
    def __str__(self):
        # Join errors into a single string rather than displaying them as a list
        return " ".join([str(e) for e in self])


class TaskForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Regular'),  # Filter for regular users
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes for multiple selections
        required=True
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'status', 'priority', 'assigned_users']  # Use 'assigned_users' here


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=[('admin', 'Admin'), ('regular', 'Regular')], required=True)
    admin_code = forms.CharField(required=False, max_length=4, widget=forms.PasswordInput)

    error_class = SingleError  # Use SingleError class for this form

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'admin_code']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")
        admin_code = cleaned_data.get("admin_code")

        # If user selected "Admin", ensure the admin code is correct
        if user_type == 'admin' and admin_code != '1234':
            # Add the error directly to the 'admin_code' field's errors
            self.add_error('admin_code', "Invalid Admin Code")

        return cleaned_data

