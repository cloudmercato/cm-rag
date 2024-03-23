import re
import sys
import logging

from llama_index.core import Settings
from llama_index.core.output_parsers.selection import SelectionOutputParser

from django.conf import settings

from core.qengines import RouterManager
from core.llm import OllamaManager

REG_JSON = re.compile('({.*})', flags=re.MULTILINE)


def set_log_verbosity(level):
    logging.basicConfig(stream=sys.stdout, level=40-level*10)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


class JsonSelectionOutputParser(SelectionOutputParser):
    def parse(self, output):
        json_text = REG_JSON.sub(output, '\1')
        return super().parse(json_text)


def get_query_engine(
    embed_dim=settings.DEFAULT_EMBED_DIM,
    ollama_model=settings.DEFAULT_OLLAMA_MODEL,
    query_engine='router',
    similarity_top_k=settings.DEFAULT_SIMILARITY_TOP_K,
    temperature=settings.DEFAULT_TEMPERATURE,
    verbose=False,
):
    ollama_manager = OllamaManager(
        model=ollama_model,
        temperature=temperature,
    )
    Settings.llm = ollama_manager.ollama

    router_manager = RouterManager(
        verbose=verbose,
    )

    if query_engine == 'router':
        query_engine = router_manager.router_query_engine
    elif query_engine == 'subquestion':
        query_engine = router_manager.subquestion_query_engine
    elif query_engine == 'recursive-retriever':
        query_engine = router_manager.sql_manager.query_engine
    elif query_engine == 'vector':
        query_engine = router_manager.vector_manager.query_engine
    elif query_engine == 'sql':
        query_engine = router_manager.sql_manager.query_engine
    elif query_engine == 'sql-retriever':
        query_engine = router_manager.sql_manager.retriever_query_engine
    return query_engine
