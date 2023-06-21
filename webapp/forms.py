from django import forms
import re

class DotplotForm(forms.Form):
    sequence1 = forms.CharField()
    sequence2 = forms.CharField()

    def is_valid(self):
        valid = self.is_valid()

        sequence1 = self.cleaned_data.get('sequence1', '')
        sequence2 = self.cleaned_data.get('sequence2', '')

        sequence1_valid = re.match(r'^[A-Za-z]+$', sequence1)
        sequence2_valid = re.match(r'^[A-Za-z]+$', sequence2)

        if not sequence1_valid:
            self.add_error('sequence1', 'Nur lateinische Buchstaben sind erlaubt.')
        if not sequence2_valid:
            self.add_error('sequence2', 'Nur lateinische Buchstaben sind erlaubt.')

        return valid and sequence1_valid and sequence2_valid
