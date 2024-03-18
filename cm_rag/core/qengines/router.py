from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core import get_response_synthesizer
from llama_index.core.selectors import LLMSingleSelector, LLMMultiSelector

from django.conf import settings
from django.utils.functional import cached_property

from core.qengines.vectors import VectorIndexManager
from core.qengines.sql import SqlManager


class RouterManager:
    def __init__(
        self,
        similarity_top_k=settings.DEFAULT_SIMILARITY_TOP_K,
        use_async=True,
        verbose=True
    ):
        self.similarity_top_k = similarity_top_k
        self.use_async = use_async
        self.verbose = verbose

    @cached_property
    def vector_manager(self):
        return VectorIndexManager()

    @cached_property
    def sql_manager(self):
        return SqlManager()

    @cached_property
    def tools(self):
        tools = []
        tools += self.vector_manager.tools
        tools += self.sql_manager.tools
        return tools

    @cached_property
    def query_engine_dict(self):
        return {
            'sql': self.sql_manager.query_engine,
        }

    @cached_property
    def router_query_engine(self):
        query_engine = RouterQueryEngine(
            selector=LLMMultiSelector.from_defaults(),
            query_engine_tools=self.tools,
            verbose=self.verbose,
        )
        return query_engine

    @cached_property
    def subquestion_query_engine(self):
        query_engine = SubQuestionQueryEngine.from_defaults(
            query_engine_tools=self.tools,
            use_async=self.use_async,
            verbose=self.verbose,
        )
        return query_engine

    @cached_property
    def recursive_retriver_query_engine(self):
        index = self.vector_manager.index
        vector_retriever = index.as_retriever(
            similarity_top_k=self.similarity_top_k,
        )
        recursive_retriever = RecursiveRetriever(
            "vector",
            retriever_dict={"vector": vector_retriever},
            query_engine_dict=query_engine_dict,
            verbose=self.verbose,
        )
        response_synthesizer = get_response_synthesizer()
        query_engine = RetrieverQueryEngine.from_args(
            recursive_retriever,
            response_synthesizer=response_synthesizer
        )
        return query_engine
