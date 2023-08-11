from django import forms
import re
class HorspoolForm(forms.Form):
    pattern = forms.CharField(label='Muster', strip=False, widget=forms.TextInput(attrs={"class": "max-width-input"}))
    sequence = forms.CharField(label='Sequenz', widget=forms.Textarea(attrs={"class": "max-width-input"}), strip=False)
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
    sequence1 = forms.CharField(label = "Sequenz 1", max_length=200, widget=forms.TextInput(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label = "Sequenz 2", max_length=200, widget=forms.TextInput(attrs={"class": "max-width-input"}))
    ignore_case_choice = forms.BooleanField(label='Groß-/Kleinschreibung ignorieren', required=False, initial=False, widget=forms.CheckboxInput())

    
    def clean(self):
        cleaned_data = super().clean()
        sequence1 = cleaned_data.get('sequence1','')
        sequence2 = cleaned_data.get('sequence2','')
        ignore_case_choice = cleaned_data.get('ignore_case_choice')
        if ignore_case_choice:
             cleaned_data['sequence1'] = sequence1.lower()
             cleaned_data['sequence2'] = sequence2.lower()
        return cleaned_data

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
    pattern = forms.CharField(label='Muster', strip=False,widget=forms.TextInput(attrs={"class": "max-width-input"}))
    sequence = forms.CharField(label='Sequenz', widget=forms.Textarea(attrs={"class": "max-width-input"}), strip=False)
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
    sequence1 = forms.CharField(label='Sequenz 1', widget=forms.TextInput(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label='Sequenz 2', widget=forms.TextInput(attrs={"class": "max-width-input"}))
    match = forms.FloatField(label='Match', min_value=-1000, max_value=1000, initial=-1)
    mismatch = forms.FloatField(label='Mismatch', min_value=-1000, max_value=1000, initial=1)
    gap_penalty = forms.FloatField(label='Gap-Score', min_value=-1000, max_value=1000, initial=1)
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
    
class SmithWatermanForm(forms.Form):
    sequence1 = forms.CharField(label='Sequenz 1', widget=forms.TextInput(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label='Sequenz 2', widget=forms.TextInput(attrs={"class": "max-width-input"}))
    match = forms.FloatField(label='Match', min_value=-1000, max_value=1000, initial=1)
    mismatch = forms.FloatField(label='Mismatch', min_value=-1000, max_value=1000, initial=-1)
    gap_penalty = forms.FloatField(label='Gap-Score', min_value=-1000, max_value=1000, initial=1)

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
    sequence1 = forms.CharField(label='Sequenz 1', widget=forms.TextInput(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label='Sequenz 2', widget=forms.TextInput(attrs={"class": "max-width-input"}))
    match = forms.FloatField(label='Match', min_value=-1000, max_value=1000, initial=0)
    mismatch = forms.FloatField(label='Mismatch', min_value=-1000, max_value=1000, initial=1)
    gap_penalty = forms.FloatField(label='Gap-Score', min_value=-1000, max_value=1000, initial=1)
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
    
class GlocalAlignmentForm(forms.Form):
    sequence1 = forms.CharField(label='Sequenz 1', widget=forms.TextInput(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label='Sequenz 2', widget=forms.TextInput(attrs={"class": "max-width-input"}))
    match = forms.FloatField(label='Match', min_value=-1000, max_value=1000, initial=-1)
    mismatch = forms.FloatField(label='Mismatch', min_value=-1000, max_value=1000, initial=1)
    gap_penalty = forms.FloatField(label='Gap-Score', min_value=-1000, max_value=1000, initial=1)
    threshold = forms.FloatField(label='Schwellenwert', min_value=-1000, max_value=1000, initial=1)
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

class ViterbiForm(forms.Form):
    sequence = forms.CharField(label='Sequenz')
    states = forms.CharField(label='Zustände')

    def clean(self):
        cleaned_data = super().clean()
        states = cleaned_data.get('states')
        states = states.split(';')
        states_to_remove = []
        for state in states:
            if state.lower() == 'start':
                states_to_remove.append(state)

        for state in states_to_remove:
            states.remove(state)    
        modified_states = states  

        cleaned_data['states'] = modified_states
        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()
        if valid:
            sequence = self.cleaned_data.get('sequence', '')
            print('seq ',sequence)
            if sequence:
                if not sequence.isalpha():
                    self.add_error('sequence', "Nur Buchstaben sind erlaubt.")
                    valid = False
            states = self.cleaned_data.get('states', '')
            if states:
                states_count = len(states)
                if states_count > 10 or states_count < 2:
                    self.add_error('states', "Geben Sie nicht mehr als 10  und nicht weniger als 2 Zustände ein, separiert mit Semikolon. Eingegebener 'Start'-Zustand wird nicht berücksichtigt.")
                    valid = False
        return valid