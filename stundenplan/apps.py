from django.apps import AppConfig


class StundenplanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stundenplan'
    
    def ready(self):
        import stundenplan.signals