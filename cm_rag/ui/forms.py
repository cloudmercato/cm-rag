from django import forms


class QueryForm(forms.Form):
    q = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'q-input',
            'placeholder': "Message Jean-Claude",
            'rows': 2,
        })
    )
