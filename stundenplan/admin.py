from pydoc import describe
from django.utils.html import format_html
from django.templatetags.static import static
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.templatetags.static import static
from django.contrib import admin
from django.core.management import call_command
from django.contrib import messages
from .models import Teacher, Grade, Class, Subject, Subject_Grade, Lesson, UserProfile, Room, StundentDataImport


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "short_name")
    search_fields = ("first_name", "last_name", "short_name")

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ( "grade", "name", "schueleranzahl", "schueler_in_class")
    search_fields = ( "grade", "name", "schueleranzahl", "schueler_in_class")
    list_filter = ("grade", "name",)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("abkuerzung", "name")
    search_fields = ("abkuerzung", "name")

@admin.register(Subject_Grade)
class SubjectGradeAdmin(admin.ModelAdmin):
    list_display = ("subject", "grade", "wochenstunden")
    search_fields = ("subject", "grade", "wochenstunden")
    list_filter = ("subject", "grade",)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "lesson_number", "weekday", "teacher", "klasse", "subject", "room_number")
    search_fields = ("lesson_number", "weekday")
    list_filter = ("weekday", "teacher", "klasse", "subject", "room_number")

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_number",)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'klasse')
    list_filter = ("klasse__grade", "klasse__name",)
    actions = ['next_year', 'assign_user_to_class']

    @admin.action(description="Ein Jahr weiter springen")
    def next_year(self, request, queryset):
        for profile in queryset:
            current_grade = profile.klasse.grade
            if current_grade.name < 12:
                new_grade_name = current_grade.name + 1
                new_grade, created = Grade.objects.get_or_create(name=new_grade_name)
                profile.klasse.grade = new_grade
                profile.klasse.save()
                profile.save()
            else:
                self.message_user(request,f"{profile.user.username} ist bereits in der höchsten Klasse angelangt und kann nicht in eine höhere Klasse versetzt werden!", level='error')

    @admin.action(description="Nutzer einer 7. Klasse zuordnen")
    def assign_user_to_class(self, request, queryset):

        seventh_grade_classes = Class.objects.filter(grade__name=7).order_by('name')

        if not seventh_grade_classes.exists():
            self.message_user(request, "Es gibt keine Klassen der 7. Stufe.", level='error')
            return

        for profile in queryset:

            for klasse in seventh_grade_classes:

                print(klasse.schueler_in_class)
                if klasse.schueler_in_class < klasse.schueleranzahl:

                    profile.klasse = klasse
                    profile.save()

                    klasse.schueler_in_class += 1
                    print(klasse.schueler_in_class)
                    klasse.save()

                    self.message_user(request, f"{profile.user.username} wurde der Klasse {klasse.name} zugeordnet.",
                                      level='success')
                    break
            else:
                self.message_user(request, f"Keine Klasse der 7. Stufe hat mehr Platz für {profile.user.username}.",
                                  level='error')


@admin.register(StundentDataImport)
class StudentDataImportAdmin(admin.ModelAdmin):
    list_display = ["name"]
    actions = ['assign_user']

    def changelist_view(self, request, extra_context=None):
        if self.model == StundentDataImport:
            extra_context = extra_context or {}
            extra_context['custom_text'] = format_html(
                """
                <div style="margin-bottom: 80px; padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd;">
                    <p>Hier kanns du .csv Dateien hochladen. Achte dabei dartuf, diese Form einzualten. Die erste Zeile deiner Datei wirdn nicht mitgelesen!</p>
                    <img src="{}" alt="Beispielbild" style="max-width: 100%; height: auto;">
                </div>
                """,
                static("Tabellenbeschreiung.png")
            )
        return super().changelist_view(request, extra_context=extra_context)

    @admin.action(description="Schüler aus Namensliste erstellen")
    def assign_user(self, request, queryset):
        for data_import in queryset:
            try:
                call_command("create_users", data_import.file.path)
                messages.success(request, f"Das Skript wurde erfolgreich mit der Datei {data_import.file.name} ausgeführt.")
            except Exception as e:
                messages.error(request, f"Fehler beim Ausführen des Skripts mit der Datei {data_import.file.name}: {e}")