from django.contrib import admin
from .models import Teacher, Grade, Class, Subject


@admin.register(Teacher)
class Teacher(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "short_name")
    search_fields = ("first_name", "last_name", "short_name")
    
    
@admin.register(Grade)
class Grade(admin.ModelAdmin):
    list_display = ("grade",)
    search_fields = ("grade",)
    
@admin.register(Class)
class Class(admin.ModelAdmin):
    list_display = ("name", "schueleranzahl")
    search_fields = ("name", "schueleranzahl")
    
@admin.register(Subject)
class Subject(admin.ModelAdmin):
    list_display = ("abkuerzung", "name")
    search_fields = ("abkuerzung", "name")