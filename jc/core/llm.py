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
        base_url=settings.OLLAMA_BASE_URL,
    ):
        self.temperature = temperature
        self.sql_temperature = sql_temperature
        self.subq_temperature = subq_temperature
        self.model = model
        self.base_url = base_url

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
            base_url=self.base_url,
            request_timeout=60.0,
        )

    @cached_property
    def sql_ollama(self):
        return Ollama(
            model=self.model,
            temperature=self.sql_temperature,
            base_url=self.base_url,
            request_timeout=60.0,
        )

    @cached_property
    def subquestion_ollama(self):
        return Ollama(
            model=self.model,
            temperature=self.subq_temperature,
            base_url=self.base_url,
            request_timeout=60.0,
        )
