from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'major', 'created_at')
    search_fields = ('name', 'email', 'major')
    list_filter = ('created_at', 'major')
