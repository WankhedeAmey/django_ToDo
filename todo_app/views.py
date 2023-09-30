from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, auth
from .forms import UserRegistrationForm, ToDoListForm, TaskForm
from django.contrib import messages
from .models import ToDoList, Task
from django.utils import timezone  # Import timezone

# Create your views here.
def index(request) :
    if request.method == 'POST':
        # Handle login request
        username = request.POST['username']
        password = request.POST['password']
    
        user = auth.authenticate(request, username=username, password=password)
    
        if user is not None:
            auth.login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, "Credentials do not match. Please try again with correct credentials.")
            return redirect('index')
    
    # Regular GET request (display the index page)
    return render(request, 'index.html')

def register(request) :
    # a user registration form with user details. Then they are getting verified for uniqueness.
    # if success, go back to index page for login
    if request.method == 'POST' :
        form = UserRegistrationForm(request.POST)
        if form.is_valid() :
            user = form.save()
            return redirect('index')
        else :
            for field, errors in form.errors.items() :
                for error in errors :
                    messages.info(request, f"Error in {field} : {error}")
    else :
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form' : form})

def homepage(request) :
    selected_list_name = None
    selected_list_id   = None
    task_form = TaskForm()
    if request.method =='POST':
        action = request.POST.get('action')
        
        # differentiate between different POST responses through action tag
        
        if action == 'select_list' :
            selected_list_id = request.POST['selected_list']
            if selected_list_id :
                __selected_list = ToDoList.objects.get(id=selected_list_id)
                if __selected_list :
                    selected_list_name = __selected_list.title
        elif action == 'create_task' :
            task_form = TaskForm(request.POST)
            if  task_form.is_valid() :
                selected_list_id = request.POST.get('selected_list_id')
                if selected_list_id :
                    selected_list = ToDoList.objects.get(id=selected_list_id)
                    if selected_list :
                        #create new task
                        new_task = task_form.save(commit=False)
                        new_task.todolist = selected_list
                        new_task.save()
                        #task_form = TaskForm
    
    # fetching user's current lists
    user_lists = ToDoList.objects.filter(user=request.user)
    form       = ToDoListForm()
    tasks = [] 
    if selected_list_id:
        selected_list = ToDoList.objects.get(id=selected_list_id)
        if selected_list :
            tasks = Task.objects.filter(todolist=selected_list)
    return render(request, 'homepage.html', {'user_lists' : user_lists, 
                                             'form' : form, 
                                             'username' : request.user.username,
                                            'selected_list_name' : selected_list_name,
                                            'selected_list_id' : selected_list_id,
                                            'task_form' : task_form,
                                            'tasks' : tasks})


# Create a new list according to user's need
def create_list(request) :
    if request.method == "POST" :
        form = ToDoListForm(request.POST)
        if form.is_valid() :
            new_list = form.save(commit=False)
            new_list.user = request.user
            new_list.save()
            return redirect('homepage')
    else :
        form = ToDoListForm()
    return render(request, 'create_list.html', {'form' : form})


def custom_logout(request):
    logout(request)
    return redirect('index')

def delete_list(request, list_id) :
    todolist = get_object_or_404(ToDoList, id = list_id)
    
    if  todolist.user == request.user :
        todolist.delete()
    return redirect('homepage')

def delete_task(request, task_id) :
    task = get_object_or_404(Task, id = task_id)
    
    if  task.todolist.user == request.user :
        task.delete()
    return redirect('homepage')


    