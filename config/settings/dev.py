"""Configurações de desenvolvimento local."""

from .base import *  # noqa: F401,F403
from .base import env_bool, env_list

DEBUG = env_bool("DJANGO_DEBUG", True)

# TEMPORARIO: avanca as etapas do formulario de incubacao sem validar (revisao de design).
# Para voltar ao normal: defina INCUBATION_SKIP_VALIDATION=0 ou remova este bloco.
INCUBATION_SKIP_VALIDATION = env_bool("INCUBATION_SKIP_VALIDATION", True)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
