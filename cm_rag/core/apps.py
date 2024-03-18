from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        Settings.embed_model = HuggingFaceEmbedding(
        )
        Settings.llm = Ollama(
            model='llama2-uncensored',
        )
