from django.contrib import admin
from .models import Name
from .models import Teacher
from .models import Class

admin.site.register(Name)
admin.site.register(Teacher)
admin.site.register(Class)
