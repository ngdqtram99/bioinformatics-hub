from django import forms
import re

class DotplotForm(forms.Form):
    sequence1 = forms.CharField(label='Sequence 1') #max_length = ?
    sequence2 = forms.CharField(label='Sequence 2')
    
    def is_valid(self):
        valid = super().is_valid()

        sequence1 = self.cleaned_data.get('sequence 1')
        sequence2 = self.cleaned_data.get('sequence 2')

        sequence1_valid = re.match(r'^[A-Za-z]+$', sequence1)
        sequence2_valid = re.match(r'^[A-Za-z]+$', sequence2)

        if not sequence1_valid:
            self.add_error('sequence 1', 'Nur lateinische Buchstaben sind erlaubt.')
        if not sequence2_valid:
            self.add_error('sequence 2', 'Nur lateinische Buchstaben sind erlaubt.')