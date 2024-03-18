from urllib.parse import urlparse

import psycopg2
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores import postgres
from llama_index.core.tools import QueryEngineTool

from django.conf import settings
from django.utils.functional import cached_property

from core import models

TABLE_NAME = "cm_vectors"


class VectorIndexManager:
    def __init__(
        self,
        embed_dim=settings.DEFAULT_EMBED_DIM,
        verbose=True
    ):
        self.embed_dim = embed_dim
        self.verbose = verbose

    @cached_property
    def vector_store(self):
        url = urlparse(settings.DATABASE_URL)
        vector_store = postgres.PGVectorStore.from_params(
            database=url.path[1:],
            host=url.hostname,
            password=url.password,
            port=url.port,
            user=url.username,
            table_name=TABLE_NAME,
            embed_dim=self.embed_dim,
            hybrid_search=True,  # TODO Correct or not
            text_search_config="english",
        )
        return vector_store

    @cached_property
    def storage_context(self):
        storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store,
        )
        return storage_context

    @cached_property
    def index(self):
        index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
        )
        return index

    @cached_property
    def query_engine(self):
        return self.index.as_query_engine()

    @cached_property
    def tools(self):
        vector_tool = QueryEngineTool.from_defaults(
            query_engine=self.query_engine,
            description=f"Useful for answering semantic questions about cloud providers",
        )
        return [vector_tool]

    def setup_database(self, url, dbname):
        conn = psycopg2.connect(url)
        conn.autocommit = True
        with conn.cursor() as c:
            c.execute(f"DROP DATABASE IF EXISTS {dbname}")
            c.execute(f"CREATE DATABASE {dbname}")

    def flush_index(self):
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.autocommit = True
        with conn.cursor() as c:
            try:
                c.execute(f"DELETE FROM data_{TABLE_NAME}")
                c.execute(f"DROP TABLE data_{TABLE_NAME}")
            except psycopg2.errors.UndefinedTable:
                pass

    def update_index(self, documents):
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=self.storage_context,
            show_progress=self.verbose,
        )
        return index
