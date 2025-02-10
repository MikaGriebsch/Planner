from django.contrib import admin
from .models import Teacher, Grade, Class, Subject, Subject_Grade, Lesson, UserProfile,Room


@admin.register(Teacher)
class Teacher(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "short_name")
    search_fields = ("first_name", "last_name", "short_name")
    
    
@admin.register(Grade)
class Grade(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    
@admin.register(Class)
class Class(admin.ModelAdmin):
    list_display = ("name", "schueleranzahl")
    search_fields = ("name", "schueleranzahl")
    
@admin.register(Subject)
class Subject(admin.ModelAdmin):
    list_display = ("abkuerzung", "name")
    search_fields = ("abkuerzung", "name")

@admin.register(Subject_Grade)
class Subject(admin.ModelAdmin):
    list_display = ("subject", "grade", "wochenstunden")
    search_fields = ("subject", "grade", "wochenstunden")
    

@admin.register(Lesson)
class Lesson(admin.ModelAdmin):
    list_display = ("id","lesson_number", "weekday", "teacher", "klasse", "subject", "room_number")
    search_fields = ("lesson_number", "weekday")
    
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_number",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'klasse')

admin.site.register(UserProfile, UserProfileAdmin)
