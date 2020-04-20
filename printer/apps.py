from django.apps import AppConfig


class PrinterConfig(AppConfig):
    name = 'printer'

    def ready(self):
        import printer.signals


