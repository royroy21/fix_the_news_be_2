from django.apps import AppConfig


class CommunicationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'fix_the_news.communications'

    def ready(self):
        """ method just to import the signals """
        import fix_the_news.communications.signals
