from django.apps import AppConfig


class FinanceiroConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "financeiro"
