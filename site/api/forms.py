from django import forms


class SearchForm(forms.Form):
    """Search by free text"""
    text = forms.CharField(
        max_length=100,
    )
