#!/usr/bin/env python
import argparse
import logging
from urllib.parse import urlparse
import sys

import psycopg2
from llama_index.core import Settings
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores import postgres
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

PERSIST_DIR = "./storage"
POSTGRES_URL = 'postgresql://ai:ai@localhost:5432'
POSTGRES_DBNAME = 'ai'
OLLAMA_MODEL = 'llama2'
DEFAULT_QUERY = "What is the top 3 data you can retrieve about price and performance for each provider?"


def setup_database(url, dbname):
    conn = psycopg2.connect(url)
    conn.autocommit = True
    with conn.cursor() as c:
        c.execute(f"DROP DATABASE IF EXISTS {dbname}")
        c.execute(f"CREATE DATABASE {dbname}")


def get_index(url, dbname, documents, embed_dim):
    url = urlparse(url)
    vector_store = postgres.PGVectorStore.from_params(
        database=dbname,
        host=url.hostname,
        password=url.password,
        port=url.port,
        user=url.username,
        table_name="cm_vectors",
        embed_dim=embed_dim
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )
    return index


def main():
    parser = argparse.ArgumentParser(description='Cloud Mercato RAG CLI')
    parser.add_argument('action', nargs='?', default='train')
    parser.add_argument('-c', '--chunk-size', type=int, default=512)
    parser.add_argument('-m', '--embed-dim', type=int, default=384)
    parser.add_argument('-o', '--ollama-model', default=OLLAMA_MODEL)
    parser.add_argument('-p', '--postgres-url', default=POSTGRES_URL)
    parser.add_argument('-P', '--postgres-dbname', default=POSTGRES_DBNAME)
    parser.add_argument('-q', '--query', default=DEFAULT_QUERY)
    parser.add_argument('-v', '--verbose', default=0)

    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=50-args.verbose*10)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    if args.action == 'train':
        Settings.llm = Ollama(
            model=args.ollama_model,
            request_timeout=60.0,
        )
        Settings.embed_model = HuggingFaceEmbedding(
        )

        documents = SimpleDirectoryReader("data").load_data()
        index = get_index(
            url=args.postgres_url,
            dbname=args.postgres_dbname,
            documents=documents,
            embed_dim=args.embed_dim,
        )

        query_engine = index.as_query_engine()
        response = query_engine.query(args.query)
        print(response.response)
    elif args.action == 'setup':
        setup_database(
            url=args.postgres_url,
            dbname=args.postgres_dbname,
        )


if __name__ == '__main__':
    main()
