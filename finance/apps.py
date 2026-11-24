from django.apps import AppConfig


class FinanceConfig(AppConfig):
    name = 'finance'

    def ready(self):
        # Import etmezsek signals.py hic calismaz, dolayisiyla signal'lar kayit olmaz.
        # Degiskeni kullanmadigimiz icin editor uyarir; # noqa onu susturur.
        from . import signals  # noqa
