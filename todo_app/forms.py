from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ToDoList, Task

# form for registration of User
class UserRegistrationForm(UserCreationForm) :
    email = forms.EmailField(max_length=250, required = True, help_text="Required. Enter a valid email address.")
    class Meta :
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_username(self) :
        username = self.cleaned_data['username']
        if User.objects.filter(username = username).exists() :
            raise forms.ValidationError("This username is already taken. Please choose a different username.")
        return username
    
    def clean_email(self) :
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists() :
            raise forms.ValidationError("This email address is already registered. Please use different email address.")
        return email

# form for creating a new list 
class ToDoListForm(forms.ModelForm) :
    class Meta :
        model  = ToDoList
        fields = ['title']
        label  = {
            'title' : 'List Title'
        }

# form for creating a new task
class TaskForm(forms.ModelForm) :
    class Meta :
        model = Task
        fields = ['title', 'task_desc']
