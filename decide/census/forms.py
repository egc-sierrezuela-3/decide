from django import forms

class votacionForm(forms.Form):
    votacion = forms.IntegerField(label='Id de la votación', widget=forms.TextInput, required=True)
