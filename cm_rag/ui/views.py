from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import BaseFormView

from core import utils
from ui import forms


class HomeView(TemplateView):
    template_name = "home.html"



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
