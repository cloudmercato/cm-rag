from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import BaseFormView

from django_tables2 import SingleTableView, SingleTableMixin
from sqlalchemy.orm import sessionmaker, scoped_session
from psycopg2 import errors as pg_errors
from sqlalchemy.sql import text

from core import utils
from core import models
from core.qengines import SqlManager
from ui import forms
from ui import tables


class HomeView(TemplateView):
    template_name = "home.html"


class ListView(SingleTableView):
    template_name = "model_list.html"

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


class VectorListView(SingleTableMixin, TemplateView):
    template_name = "model_list.html"
    table_class = tables.VectorTable

    @property
    def table_data(self):
        sql_manager = SqlManager()
        Session = scoped_session(sessionmaker(bind=sql_manager.engine))
        session = Session()
        try:
            response = session.execute(text('SELECT * FROM data_cm_vectors;'))
        except pg_errors.ProgrammingError as err:
            return []
        except pg_errors.UndefinedTable as err:
            return []
        return response.mappings()

    def get_context_data(self):
        context = super().get_context_data()
        opts = {
            'verbose_name_plural': 'vectors',
        }
        context.update(
            opts=opts,
        )
        return context


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
            context['error'] = err

        return render(
            request=self.request,
            template_name=self.template_name,
            context=context,
        )
