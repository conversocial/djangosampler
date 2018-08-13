from __future__ import absolute_import

from django.apps import AppConfig
from . import plugins


class DjangoSamplerConfig(AppConfig):
    name = 'djangosampler'
    verbose_name = 'Django Sampler'

    def ready(self):
        plugins.install_plugins()
