from django import forms
import re
class HorspoolForm(forms.Form):
    pattern = forms.CharField(label='Muster')
    sequence = forms.CharField(label='Sequenz', widget=forms.Textarea)
    direction = forms.ChoiceField(
        label='Richtung',
        choices=[('forward', 'Vorwärts'), ('backward', 'Rückwärts')],
        widget=forms.RadioSelect
    )
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
                 self.add_error('pattern', 'Pattern darf nicht länger als Sequenz sein')
            return valid and pattern_valid and sequence_valid
import re

class DotplotForm(forms.Form):
    sequence1 = forms.CharField(max_length=200)
    sequence2 = forms.CharField(max_length=200)

    def is_valid(self):
        valid = super().is_valid()

        sequence1 = self.cleaned_data.get('sequence1', '')
        sequence2 = self.cleaned_data.get('sequence2', '')

        sequence1_valid = re.match(r'^[A-Za-z]+$', sequence1)
        sequence2_valid = re.match(r'^[A-Za-z]+$', sequence2)

        if not sequence1_valid:
            self.add_error('sequence1', 'Nur lateinische Buchstaben sind erlaubt.')
        if not sequence2_valid:
            self.add_error('sequence2', 'Nur lateinische Buchstaben sind erlaubt.')

        return valid and sequence1_valid and sequence2_valid
    
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
    
class OverlapForm(forms.Form):
    sequence1 = forms.CharField(label='Sequenz 1')
    sequence2 = forms.CharField(label='Sequenz 2')
    match = forms.IntegerField(label='Match', min_value=-100, max_value=100, initial=1)
    mismatch = forms.IntegerField(label='Mismatch', min_value=-100, max_value=100, initial=-1)
    gap_penalty = forms.IntegerField(label='Gap-Score', min_value=-100, max_value=100, initial=-1)

    def is_valid(self):
            valid = super().is_valid()

            sequence1 = self.cleaned_data.get('sequence1', '')
            sequence2 = self.cleaned_data.get('sequence2', '')

            sequence1_valid = re.match(r'^[A-Za-z]+$', sequence1)
            sequence2_valid = re.match(r'^[A-Za-z]+$', sequence2)

            if not sequence1_valid:
                self.add_error('sequence1', 'Nur lateinische Buchstaben sind erlaubt.')
            if not sequence2_valid:
                self.add_error('sequence2', 'Nur lateinische Buchstaben sind erlaubt.')
            

            return valid and sequence1_valid and sequence2_valid