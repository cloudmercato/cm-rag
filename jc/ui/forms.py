from django import forms


QUERY_ENGINES = (
    ('router', "Router"),
    ('subquestion', "Sub-question"),
    ('recursive-retriever', "Recursive retriever"),
    ('vector', "Vector"),
    ('sql', "SQL database"),
    ('sql-retriever', "SQL retriever"),
    ('kg', "Knowledge graph"),
)

class QueryForm(forms.Form):
    q = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'q-input',
            'placeholder': "Message Jean-Claude",
            'rows': 2,
        })
    )
    query_engine = forms.ChoiceField(
        initial="sql-retriever",
        choices=QUERY_ENGINES,
    )
    similarity_top_k = forms.IntegerField(
        min_value=1,
        max_value=16,
        initial=4,
    )
    temperature = forms.FloatField(
        min_value=0,
        max_value=1,
        step_size=.05,
        initial=.5,
    )
