from django.apps import AppConfig
//this is app field in this section

class XssVulnerableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xss_vulnerable'
