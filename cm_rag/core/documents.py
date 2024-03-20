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

from django.conf import settings

from core import files
from core import data
from core import models


class DocumentManager:
    def __init__(self):
        self.files = files.FileManager()

    @property
    def provider_wiki_docs(self):
        providers = models.Provider.objects.values_list('name', flat=True)
        wiki_docs = []
        wiki_errors = (wiki_exceptions.PageError, wiki_exceptions.DisambiguationError)
        for provider in providers:
            try:
                wiki_docs += WikipediaReader().load_data(pages=[provider])
            except wiki_errors as err:
                print(err)
        return wiki_docs

    def get_provider_documents(self, update=False, concat_rows=False):
        csv_reader = PandasCSVReader(
            concat_rows=concat_rows,
        )

        name = 'providers'
        self.files.download(name, update=update)
        filename = self.files.make_filename(name)
        documents, nodes = [], []

        df = pd.read_csv(filename)
        for idx, row in df.iterrows():
            doc_id = f"{row['name']}"
            text = row['name']
            doc = Document(text=text, doc_id=doc_id, extra_info={
                'short name': row['short_name'],
            })
            documents.append(doc)

            text = "%(name)s also known as %(short_name)s is a cloud provider." % {
                'name': row['name'],
                'short_name': row.short_name,
            }
            if row.Headquarters not in ('nan', ):
                text += f" With headquarters in {row.Headquarters}."

            doc_id = f"{row['name']}-details"
            doc = Document(text=text, doc_id=doc_id, extra_info={
                
            })
            documents.append(doc)

        text = f"Cloud Mercato's database counts {df.shape[0]}) providers: "
        text += ' '.join(df['name'].values)
        doc = Document(text=text)
        documents.append(doc)

        return documents, nodes

    def get_flavor_index_node(self, docs):
        idx_node = IndexNode(
            text="This node providers information about the flavor catalog",
            index_id='flavors',
        )
        return idx_node

    def get_flavor_documents(self, update=False, concat_rows=False):
        name = 'flavors'
        documents, nodes = [], []
        self.files.download(name, update=update)
        filename = self.files.make_filename(name)

        csv_reader = PandasCSVReader(
            concat_rows=concat_rows,
        )
        documents += csv_reader.load_data(filename)

        df = pd.read_csv(filename)

        archs = df[df.Arch.notna()].Arch.unique()
        for arch in archs:
            doc = Document(text=arch, doc_id=arch, extra_info={})
            documents.append(doc)

        cpus = df.CPU.unique()
        for cpu in cpus:
            doc_id = f"{cpu}-cpu" 
            text = f"{cpu} CPU" + ('s' if cpu>1 else '')
            doc = Document(text=text, doc_id=doc_id, extra_info={})
            documents.append(doc)

        for idx, row in df.iterrows():
            text = "%(name)s is a %(type)s flavor sold by %(provider)s." % {
                'name': row.Name,
                'type': row.Type,
                'provider': row.Provider,
            }
            text += " It has %(cpu)s CPU(s) and %(ram)sMB of memory powered by %(arch)s architecture." % {
                'cpu': row.CPU,
                'ram': row.RAM,
                'arch': row.Arch,
            }
            doc_id = f"{row.Provider}/{row.Name}"
            doc = Document(text=text, doc_id=doc_id, extra_info={
                'provider': row.Provider,
                'cpu-number': row.CPU,
            })
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

        docs, ns = self.get_provider_documents(update, concat_rows)
        documents += docs
        # nodes += ns
        # docs, ns = self.get_flavor_documents(update, concat_rows)
        # documents += docs
        # nodes += ns

        documents += self.provider_wiki_docs

        return documents, nodes
