from llama_index.llms.ollama import Ollama
from django.conf import settings
from django.utils.functional import cached_property


class OllamaManager:
    def __init__(
        self,
        temperature=settings.DEFAULT_TEMPERATURE,
        sql_temperature=settings.DEFAULT_SQL_TEMPERATURE,
        subq_temperature=settings.DEFAULT_SUBQ_TEMPERATURE,
        model=settings.DEFAULT_OLLAMA_MODEL,
    ):
        self.temperature = temperature
        self.sql_temperature = sql_temperature
        self.subq_temperature = subq_temperature
        self.model = model

    @property
    def system_prompt(self):
        with open(settings.SYSTEM_PROMPT) as fd:
            return fd.read().strip()

    @cached_property
    def ollama(self):
        return Ollama(
            system_prompt=self.system_prompt,
            model=self.model,
            temperature=self.temperature,
            request_timeout=60.0,
        )

    @cached_property
    def sql_ollama(self):
        return Ollama(
            system_prompt=None,
            model=self.model,
            temperature=self.sql_temperature,
            request_timeout=60.0,
        )

    @cached_property
    def subquestion_ollama(self):
        return Ollama(
            system_prompt=None,
            model=self.model,
            temperature=self.subq_temperature,
            request_timeout=60.0,
        )
