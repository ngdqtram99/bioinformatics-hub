from django import forms

class ViterbiForm(forms.Form):
    sequence = forms.CharField(label='Sequenz')
    states = forms.CharField(label='Zustände')