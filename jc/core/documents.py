import os

import pandas as pd
import wikipedia
from wikipedia import exceptions as wiki_exceptions

from llama_index.core import Document
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core.schema import IndexNode
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.readers.file import PandasCSVReader
from llama_index.readers.file import CSVReader
from llama_index.readers.web import UnstructuredURLLoader
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core.storage.docstore import SimpleDocumentStore

from django.utils.functional import cached_property
from django.conf import settings

from core.storage import StorageManager
from core.files import FileManager
from core import data
from core import models


class DocumentManager:
    def __init__(
        self,
        embed_dim=settings.DEFAULT_EMBED_DIM,
        verbose=True
    ):
        self.embed_dim = embed_dim
        self.verbose = verbose

    @cached_property
    def storage_manager(self):
        return StorageManager(
            embed_dim=self.embed_dim,
            verbose=self.verbose,
        )

    @cached_property
    def files(self):
        return FileManager()

    @cached_property
    def store(self):
        return self.storage_manager.docstore

    @cached_property
    def documents(self):
        return self.store._kvstore.get_all()

    @cached_property
    def provider_wiki_docs(self):
        providers = models.Provider.objects.values_list('name', flat=True)
        wiki_docs = []
        wiki_errors = (wiki_exceptions.PageError, wiki_exceptions.DisambiguationError)
        for provider in providers[:3]:
            try:
                wiki_docs += WikipediaReader().load_data(pages=[provider])
            except wiki_errors as err:
                print(err)
        return wiki_docs

    def get_provider_documents(self):
        documents, nodes = [], []
        providers = models.Provider.objects.all()
        # Create a doc describing the providers
        for provider in providers:
            doc_id = f"{provider.slug}-details"
            text = provider.name
            if provider.short_name and provider.short_name != provider.name:
                text += f' , also known as {provider.short_name},'
            if provider.kind:
                text += f' is a {provider.kind} cloud'
            if provider.headquarters:
                text += f' from {provider.headquarters}'
            text += '.'
            doc = Document(text=text, doc_id=doc_id, extra_info={
            })
            documents.append(doc)
        # Summary doc
        text = f"Cloud Mercato's database counts {providers.count()} providers: "
        text += ' '.join(providers.values_list('name', flat=True))
        doc = Document(text=text, doc_id='cloud-mercato-providers')
        documents.append(doc)

        return documents, nodes

    def get_flavor_index_node(self, docs):
        idx_node = IndexNode(
            text="This node provides information about the flavor catalog",
            index_id='flavors',
        )
        return idx_node

    def get_flavor_documents(self):
        documents, nodes = [], []
        flavors = models.Flavor.objects\
            .select_related('provider')\
            .all()
        # Add archs
        archs = flavors\
            .filter(arch__isnull=False)\
            .values_list('arch', flat=True).distinct()
        for arch in archs:
            doc = Document(text=arch, doc_id=arch, extra_info={})
            documents.append(doc)
        # Doc per flavor
        for flavor in flavors:
            doc_id = f"{flavor.provider.slug}-{flavor.slug}-details"
            text = f"{flavor.name} is a flavor provided by {flavor.provider.name}."
            if flavor.type:
                text += " It is a {flavor.type} with {flavor.cpu} CPU(s) and {flavor.ram} MB of RAM."
            if flavor.arch:
                text += " It is powered by a %(flavor.arch)s architecture."
            if flavor.gpu:
                text += " It has {flavor.gpu}x {flavor.gpu_model} GPU(s)"
            doc = Document(text=text, doc_id=doc_id, extra_info={
            })
        # Summary doc
        text = f"Cloud Mercato's database counts {flavors.count()} flavors."
        doc = Document(text=text, doc_id='cloud-mercato-flavors')
        documents.append(doc)

        return documents, nodes

    def get_documents(self, update=False, concat_rows=True):
        documents, nodes = [], []

        # doc = Document(text=data.CM_TEXT)
        # documents.append(doc)
        # doc = Document(text=data.SYNONYMS)
        # documents.append(doc)

        # cm_site_reader = UnstructuredURLLoader([
        #     'https://www.cloud-mercato.com',
        #     'https://www.cloud-mercato.com/faq',
        #     # 'https://p2p.cloud-mercato.com/',
        #     # 'https://projector.cloud-mercato.com/',
        # ])
        # documents += cm_site_reader.load_data()

        docs, ns = self.get_provider_documents()
        documents += docs
        nodes += ns

        docs, ns = self.get_flavor_documents()
        documents += docs
        nodes += ns

        # documents += self.provider_wiki_docs

        return documents, nodes

    def save(self, documents):
        self.store.add_documents(documents)
