from django import forms
import re
class SimpleSearchForm(forms.Form):
    pattern = forms.CharField(label='Muster')
    sequence = forms.CharField(label='Sequenz', widget=forms.Textarea)

    def is_valid(self):
            valid = super().is_valid()

            pattern = self.cleaned_data.get('pattern', '')
            sequence = self.cleaned_data.get('sequence', '')

            pattern_valid = re.match(r'^[A-Za-z]+$', pattern)
            sequence_valid = re.match(r'^[A-Za-z]+$', sequence)

            if not pattern_valid:
                self.add_error('pattern', 'Nur lateinische Buchstaben sind erlaubt.')
            if not sequence_valid:
                self.add_error('sequence', 'Nur lateinische Buchstaben sind erlaubt.')
            if len(pattern) > len(sequence):
                 pattern_valid = False
                 self.add_error('pattern', 'Pattern kann nicht länger als Sequenz sein')

            return valid and pattern_valid and sequence_valid