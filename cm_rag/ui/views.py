from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import BaseFormView

from django_tables2 import SingleTableView

from core import utils
from core import models
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



class QueryView(TemplateResponseMixin, BaseFormView):
    template_name = "query.html"
    form_class = forms.QueryForm

    def form_valid(self, form):
        q = form.cleaned_data['q']
        query_engine = utils.get_query_engine()
        response = query_engine.query(q)
        answer = response.response

        context = self.get_context_data()
        context['answer'] = answer

        return render(
            request=self.request,
            template_name=self.template_name,
            context=context,
        )
