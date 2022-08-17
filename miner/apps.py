from django.apps import AppConfig
# from .tasks import mine

class MinerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'miner'

    # def ready(self):
    #     # mine.delay()
    #     pass

