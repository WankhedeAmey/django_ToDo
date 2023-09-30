from django.contrib import admin
from .models import ToDoList, Task

# Register your models here.

#register here so that models are seen in admin panel
admin.site.register(ToDoList)
admin.site.register(Task)
