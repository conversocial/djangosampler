from django.apps import AppConfig
import plugins

class DjangoSamplerConfig(AppConfig):
    name = 'djangosampler'
    verbose_name = 'Django Sampler'

    def ready(self):
        plugins.install_plugins()
