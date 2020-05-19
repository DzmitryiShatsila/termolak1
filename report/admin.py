from django.contrib import admin
from .models import Cases
from employee.models import Profile
from tasks.models import Tasks

# Register your models here.
admin.site.register(Profile)


@admin.register(Cases)
class CasesAdmin(admin.ModelAdmin):
    list_display = ('case_code', 'date', 'author', 'product', 'software', 'images', 'procedure', 'time')
    search_fields = ('case_code', )
    list_filter = ('date', 'author', 'product', 'procedure', 'software')


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('casecode', 'author', 'deadline', 'status', 'id')

