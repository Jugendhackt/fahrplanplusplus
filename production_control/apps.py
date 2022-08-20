from django.apps import AppConfig
from django.core.signals import request_finished
from django.db.models.signals import post_delete, post_save


class ProductionControlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "production_control"

    def ready(self):
        request_finished.connect(self.signal_handler)
        post_save.connect(self.signal_handler)
        post_delete.connect(self.signal_handler)

    def signal_handler(self, sender, **kwargs):
        from production_control import broadcast

        broadcast.broadcast_status()
