"""
https://docs.llamaindex.ai/en/stable/examples/query_engine/SQLRouterQueryEngine.html
"""
from llama_index.core import SQLDatabase
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.indices.struct_store import SQLTableRetrieverQueryEngine
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.core import VectorStoreIndex

from sqlalchemy import create_engine, MetaData

from django.conf import settings
from django.utils.functional import cached_property
from django.apps import apps


class SqlManager:
    def __init__(
        self,
        similarity_top_k=settings.DEFAULT_SIMILARITY_TOP_K,
        verbose=True,
    ):
        self.similarity_top_k = similarity_top_k
        self.verbose = verbose

    @cached_property
    def engine(self):
        engine = create_engine(settings.DATABASE_URL, future=True)
        return engine

    @cached_property
    def models(self):
        return [
            m for m in apps.get_app_config('core').get_models()
        ]

    @cached_property
    def sql_tables(self):
        tables = [m._meta.db_table for m in self.models]
        return tables

    @cached_property
    def models_metadata(self):
        return {
            m._meta.model_name: {
                'primary_key': m._meta.pk.name,
                'verbose_name': m._meta.verbose_name,
                'verbose_name_plural': m._meta.verbose_name_plural,
                'db_table': m._meta.db_table,
                'fields': {
                    f.name : {
                        'name': f.name,
                        'verbose_name': f.verbose_name,
                        'help_text': f.help_text,
                    }
                    for f in m._meta.fields
                }
            }
            for m in self.models
        }

    @cached_property
    def sql_metadata(self):
        metadata = MetaData()
        metadata.reflect(
            bind=self.engine,
            only=self.sql_tables,
        )
        return metadata

    @cached_property
    def sql_database(self):
        sql_database = SQLDatabase(
            self.engine,
            include_tables=self.sql_tables,
            metadata=self.sql_metadata,
        )
        return sql_database

    @cached_property
    def query_engine(self):
        query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database,
            tables=self.sql_tables,
            verbose=self.verbose,
        )
        return query_engine

    @cached_property
    def tools(self):
        desc = "Useful for translating a natural language query into a SQL query over tables:"
        for model in self.models:
            desc += f"\n{model._meta.model_name} containing the specifications of each {model._meta.verbose_name}"
        sql_tool = QueryEngineTool.from_defaults(
            query_engine=self.query_engine,
            description=desc,
        )
        return [sql_tool]

    @cached_property
    def table_node_mapping(self):
        table_node_mapping = SQLTableNodeMapping(self.sql_database)
        return table_node_mapping

    @cached_property
    def table_schema_objs(self):
        return [
            SQLTableSchema(table_name=table_name)
            for table_name in self.sql_tables
        ]

    @cached_property
    def obj_index(self):
        table_schema_objs = []
        obj_index = ObjectIndex.from_objects(
            objects=self.table_schema_objs,
            object_mapping=self.table_node_mapping,
            index_cls=VectorStoreIndex,
        )
        return obj_index

    @cached_property
    def table_retriever(self):
        table_retriever = self.obj_index.as_retriever(
            similarity_top_k=self.similarity_top_k,
            verbose=self.verbose,
        )
        return table_retriever

    @cached_property
    def retriever_query_engine(self):
        retriever_query_engine = SQLTableRetrieverQueryEngine(
            sql_database=self.sql_database,
            table_retriever=self.table_retriever,
        )
        return retriever_query_engine
