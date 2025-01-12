from django.apps import AppConfig


class XssVulnerableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xss_vulnerable'
