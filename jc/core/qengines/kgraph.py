from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import KnowledgeGraphRAGRetriever

from django.utils.functional import cached_property

from core.llm import OllamaManager
from core.indices import KnowledgeGraphIndexManager


class KnowledgeGraphManager:
    def __init__(
        self,
        kg_triple_extract_template=None,
        max_triplets_per_chunk=10,
        include_text=True,
        response_mode='tree_summarize',
        embedding_mode='hybrid',
        similarity_top_k=4,
        verbose=True,
    ):
        # Index
        self.kg_triple_extract_template = kg_triple_extract_template
        self.max_triplets_per_chunk = max_triplets_per_chunk
        # Qengine
        self.include_text = include_text
        self.response_mode = response_mode
        self.embedding_mode = embedding_mode
        self.similarity_top_k = similarity_top_k
        self.verbose = verbose

    @cached_property
    def ollama(self):
        return OllamaManager(
        ).ollama

    @cached_property
    def index_manager(self):
        return KnowledgeGraphIndexManager(
            kg_triple_extract_template=self.kg_triple_extract_template,
            max_triplets_per_chunk=self.max_triplets_per_chunk,
            verbose=self.verbose,
        )

    @cached_property
    def index(self):
        return self.index_manager.index

    @cached_property
    def query_engine(self):
        return self.index_manager.query_engine

    @cached_property
    def graph_rag_retriever(self):
        return KnowledgeGraphRAGRetriever(
            storage_context=self.index_manager.storage_context,
            ollama=self.ollama,
            verbose=self.verbose,
        )

    @cached_property
    def retriever_query_engine(self):
        return RetrieverQueryEngine.from_args(
            retriever=self.graph_rag_retriever,
            llm=self.ollama,
        )
