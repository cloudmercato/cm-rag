import traceback

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic.base import View
from django.views.generic.base import TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import BaseFormView
from django.urls import reverse

from django_tables2 import SingleTableView, SingleTableMixin
from sqlalchemy.orm import sessionmaker, scoped_session
from psycopg2 import errors as pg_errors
from sqlalchemy.sql import text

from core import utils
from core import models
from core.qengines import SqlManager
from core.indices import IndexManager
from core.storage import StorageManager
from ui import forms
from ui import tables


class HomeView(TemplateView):
    template_name = "home.html"


class ListView(SingleTableView):
    template_name = "model_list.html"
    paginate_by = 100

    def get_context_data(self):
        context = super().get_context_data()
        context.update(
            opts=self.model._meta,
        )
        return context


class ProviderListView(ListView):
    model = models.Provider
    table_class = tables.ProviderTable


class FlavorListView(ListView):
    model = models.Flavor
    table_class = tables.FlavorTable


class IndexListView(SingleTableMixin, TemplateView):
    template_name = "model_list.html"
    table_class = tables.IndexTable
    paginate_by = 100

    @property
    def table_data(self):
        storage_manager = StorageManager()
        response = storage_manager.index_store_manager.get_all()
        return response

    def get_context_data(self):
        context = super().get_context_data()
        opts = {
            'verbose_name_plural': 'indices',
        }
        context.update(
            opts=opts,
        )
        return context


class IndexDetailView(TemplateView):
    template_name = "model_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        storage_manager = StorageManager()
        instance = storage_manager.index_store_manager.get(kwargs['key'])
        opts = {
            'verbose_name_plural': 'Indices',
        }
        context.update(
            list_url=reverse('index-list'),
            instance=instance,
            verbose=kwargs['key'],
            opts=opts,
        )
        return context


class VectorListView(SingleTableMixin, TemplateView):
    template_name = "model_list.html"
    table_class = tables.VectorTable
    paginate_by = 100

    @property
    def table_data(self):
        storage_manager = StorageManager()
        response = storage_manager.vector_store_manager.get_all()
        return response

    def get_context_data(self):
        context = super().get_context_data()
        opts = {
            'verbose_name_plural': 'vectors',
        }
        context.update(
            opts=opts,
        )
        return context


class VectorDetailView(TemplateView):
    template_name = "model_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        storage_manager = StorageManager()
        instance = storage_manager.vector_store_manager.get(kwargs['id'])
        opts = {
            'verbose_name_plural': 'Vectors',
        }
        context.update(
            list_url=reverse('vector-list'),
            instance=instance,
            verbose=kwargs['id'],
            opts=opts,
        )
        return context


class DocumentListView(SingleTableMixin, TemplateView):
    template_name = "model_list.html"
    table_class = tables.DocumentTable
    paginate_by = 100

    @property
    def table_data(self):
        storage_manager = StorageManager()
        response = storage_manager.docstore_manager.get_all()
        return response

    def get_context_data(self):
        context = super().get_context_data()
        opts = {
            'verbose_name_plural': 'Documents',
        }
        context.update(
            opts=opts,
        )
        return context


class DocumentDetailView(TemplateView):
    template_name = "model_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        storage_manager = StorageManager()
        instance = storage_manager.docstore_manager.get(kwargs['uuid'])
        opts = {
            'verbose_name_plural': 'Documents',
        }
        context.update(
            list_url=reverse('document-list'),
            instance=instance,
            verbose=kwargs['uuid'],
            opts=opts,
        )
        return context


class KnowledgeGraphView(TemplateView):
    template_name = "knowledge_graph.html"

    def get_context_data(self):
        context = super().get_context_data()
        opts = {
            'verbose_name_plural': 'Knowledge graph',
        }
        index_manager = IndexManager()
        graph = index_manager.knowledge.index.get_networkx_graph()
        context.update(
            opts=opts,
            graph=graph,
        )
        return context


class KnowledgeGraphGraphView(TemplateView):
    def get(self, request):
        from pyvis.network import Network
        index_manager = IndexManager()
        graph = index_manager.knowledge.index.get_networkx_graph()

        net = Network()
        net.from_nx(graph)
        content = net.generate_html()
        return HttpResponse(
            content=content,
        )


class QueryView(TemplateResponseMixin, BaseFormView):
    template_name = "query.html"
    form_class = forms.QueryForm

    def form_valid(self, form):
        context = self.get_context_data()
        qengine_kwargs = form.cleaned_data.copy()
        q = qengine_kwargs.pop('q')
        query_engine = utils.get_query_engine(**qengine_kwargs)

        try:
            context['response'] = query_engine.query(q)
        except ValueError as err:
            context['error'] = err
        except Exception as err:
            context['error'] = traceback.format_exc()

        return render(
            request=self.request,
            template_name=self.template_name,
            context=context,
        )
