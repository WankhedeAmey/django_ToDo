from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Import timezone


# Create your models here

#User -- Done by using default User object provided by Django


#List
class ToDoList(models.Model) :
    #some user associated with it
    #list name
    #date created
    #number of tasks
    #list of tasks? Taken care by foreign key
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title           = models.CharField(max_length=50)
    def __str__(self) :
        return self.title
    
#Task
class Task(models.Model) :
    #List associated with it
    #task name
    #task description
    todolist     = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    title        = models.CharField(max_length=50)
    task_desc    = models.CharField(max_length=200)
    completed    = models.BooleanField(default=False)
    
    def __str__(self) :
        return self.title

