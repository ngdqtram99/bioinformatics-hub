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

            if len(pattern) > len(sequence):
                 self.add_error('pattern', 'Pattern darf nicht kürzer als Sequenz sein')

            if not pattern_valid:
                self.add_error('pattern', 'Nur lateinische Buchstaben sind erlaubt.')
            if not sequence_valid:
                self.add_error('sequence', 'Nur lateinische Buchstaben sind erlaubt.')

            return valid and pattern_valid and sequence_valid