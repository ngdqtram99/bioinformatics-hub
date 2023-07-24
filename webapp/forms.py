from django import forms
import re
class HorspoolForm(forms.Form):
    pattern = forms.CharField(label='Muster', strip=False)
    sequence = forms.CharField(label='Sequenz', widget=forms.Textarea, strip=False)
    direction = forms.ChoiceField(
        label='Richtung',
        choices=[('forward', 'Vorwärts'), ('backward', 'Rückwärts')],
        widget=forms.RadioSelect
    )
    ignore_case_choice = forms.BooleanField(label='Groß-/Kleinschreibung ignorieren', required=False, initial=False, widget=forms.CheckboxInput())
    
    def clean(self):
        cleaned_data = super().clean()
        pattern = cleaned_data.get('pattern','')
        sequence = cleaned_data.get('sequence','')
        ignore_case_choice = cleaned_data.get('ignore_case_choice')
        if ignore_case_choice:
             cleaned_data['pattern'] = pattern.lower()
             cleaned_data['sequence'] = sequence.lower()
        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()

        pattern = self.cleaned_data.get('pattern', '')
        sequence = self.cleaned_data.get('sequence', '')

        if len(pattern) > len(sequence):
                valid = False
                self.add_error('pattern', 'Pattern kann nicht länger als Sequenz sein')

        return valid 

class DotplotForm(forms.Form):
    sequence1 = forms.CharField(label = "Sequenz 1", max_length=200, strip=False,widget=forms.TextInput(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label = "Sequenz 2", max_length=200, strip=False,widget=forms.TextInput(attrs={"class": "max-width-input"}))

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
    pattern = forms.CharField(label='Muster', strip=False)
    sequence = forms.CharField(label='Sequenz', widget=forms.Textarea, strip=False)
    ignore_case_choice = forms.BooleanField(label='Groß-/Kleinschreibung ignorieren', required=False, initial=False, widget=forms.CheckboxInput())
    
    def clean(self):
        cleaned_data = super().clean()
        pattern = cleaned_data.get('pattern','')
        sequence = cleaned_data.get('sequence','')
        ignore_case_choice = cleaned_data.get('ignore_case_choice')
        if ignore_case_choice:
             cleaned_data['pattern'] = pattern.lower()
             cleaned_data['sequence'] = sequence.lower()
        return cleaned_data
    
    def is_valid(self):
        valid = super().is_valid()

        pattern = self.cleaned_data.get('pattern', '')
        sequence = self.cleaned_data.get('sequence', '')

        if len(pattern) > len(sequence):
                valid = False
                self.add_error('pattern', 'Pattern kann nicht länger als Sequenz sein')

        return valid 
    
class OverlapForm(forms.Form):
    sequence1 = forms.CharField(label='Sequenz 1')
    sequence2 = forms.CharField(label='Sequenz 2')
    match = forms.IntegerField(label='Match', min_value=-100, max_value=100, initial=1)
    mismatch = forms.IntegerField(label='Mismatch', min_value=-100, max_value=100, initial=-1)
    gap_penalty = forms.IntegerField(label='Gap-Score', min_value=-100, max_value=0, initial=-1)

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
    
class NeedlemanWunschForm(forms.Form):
    sequence1 = forms.CharField(label='Sequenz 1')
    sequence2 = forms.CharField(label='Sequenz 2')
    match = forms.IntegerField(label='Match', min_value=-100, max_value=100, initial=0)
    mismatch = forms.IntegerField(label='Mismatch', min_value=-100, max_value=100, initial=1)
    gap_penalty = forms.IntegerField(label='Gap-Score', min_value=-100, max_value=100, initial=1)
    choices = [('distance', 'Distanz'), ('similarity', 'Ähnlichkeit')]
    optimization_field = forms.ChoiceField(widget=forms.RadioSelect, choices=choices, initial='distance', label='Optimieren nach:')

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