import re

from llama_index.core import Settings
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.llms.ollama import Ollama
from llama_index.core.output_parsers.selection import SelectionOutputParser

from django.conf import settings

from core.qengines import RouterManager

REG_JSON = re.compile('({.*})', flags=re.MULTILINE)


class JsonSelectionOutputParser(SelectionOutputParser):
    def parse(self, output):
        json_text = REG_JSON.sub(output, '\1')
        return super().parse(json_text)


def get_system_prompt():
    with open(settings.SYSTEM_PROMPT) as fd:
        return fd.read().strip()


def get_query_engine(
    embed_dim=settings.DEFAULT_EMBED_DIM,
    system_prompt=None,
    ollama_model=settings.DEFAULT_OLLAMA_MODEL,
    query_engine='router',
    similarity_top_k=settings.DEFAULT_SIMILARITY_TOP_K,
    temperature=settings.DEFAULT_TEMPERATURE,
    verbose=False,
):
    system_prompt = system_prompt or get_system_prompt()
    Settings.llm = Ollama(
        system_prompt=system_prompt,
        model=ollama_model,
        temperature=temperature,
        request_timeout=60.0,
    )


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
