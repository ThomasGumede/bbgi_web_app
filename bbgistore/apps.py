from django.apps import AppConfig
# from bbgistore.utilities.signals import process_uploaded_video


class BbgistoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bbgistore'
    verbose_name = "BBGI Store"
    verbose_name_plural = "BBGI Store"
    
    def ready(self):
        import bbgistore.utilities.signals
