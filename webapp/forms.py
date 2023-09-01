from django import forms
import re
class HorspoolForm(forms.Form):
    pattern = forms.CharField(label='Muster', widget=forms.TextInput(attrs={"size": "167"}))
    sequence = forms.CharField(label='Sequenz', widget=forms.TextInput(attrs={"size": "167"}))
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
                self.add_error('pattern', 'Pattern darf nicht länger als Sequenz sein')

        return valid 

class DotplotForm(forms.Form):
    sequence1 = forms.CharField(label = "Sequenz 1", max_length=200, strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label = "Sequenz 2", max_length=200, strip = False , widget=forms.Textarea(attrs={"class": "max-width-input"}))

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
    sequence = forms.CharField(label='Sequenz', strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
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
                self.add_error('pattern', 'Pattern darf nicht länger als Sequenz sein')

        return valid 
    
class OverlapForm(forms.Form):
    sequence1 = forms.CharField(label='Sequenz 1', strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label='Sequenz 2', strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
    match = forms.FloatField(label='Match', min_value=-1000, max_value=1000, initial=-1, widget=forms.TextInput(attrs={'size': '10'}))
    mismatch = forms.FloatField(label='Mismatch', min_value=-1000, max_value=1000, initial=1, widget=forms.TextInput(attrs={'size': '10'}))
    gap_penalty = forms.FloatField(label='Gap-Score', min_value=-1000, max_value=1000, initial=1, widget=forms.TextInput(attrs={'size': '10'}))
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
    sequence1 = forms.CharField(label='Sequenz 1', strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label='Sequenz 2', strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
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
    sequence1 = forms.CharField(label='Sequenz 1', strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label='Sequenz 2', strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
    match = forms.FloatField(label='Match', min_value=-1000, max_value=1000, initial=0, widget=forms.TextInput(attrs={'size': '10'}))
    mismatch = forms.FloatField(label='Mismatch', min_value=-1000, max_value=1000, initial=1, widget=forms.TextInput(attrs={'size': '10'}))
    gap_penalty = forms.FloatField(label='Gap-Score', min_value=-1000, max_value=1000, initial=1, widget=forms.TextInput(attrs={'size': '10'}))
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
    sequence1 = forms.CharField(label='Sequenz 1', strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
    sequence2 = forms.CharField(label='Sequenz 2', strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
    match = forms.FloatField(label='Match', min_value=-1000, max_value=1000, initial=-1, widget=forms.TextInput(attrs={'size': '10'}))
    mismatch = forms.FloatField(label='Mismatch', min_value=-1000, max_value=1000, initial=1, widget=forms.TextInput(attrs={'size': '10'}))
    gap_penalty = forms.FloatField(label='Gap-Score', min_value=-1000, max_value=1000, initial=1,widget=forms.TextInput(attrs={'size': '10'}))
    threshold = forms.FloatField(label='Schwellenwert', min_value=-1000, max_value=1000, initial=1, widget=forms.TextInput(attrs={'size': '10'}))
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
    sequence = forms.CharField(label='Sequenz', strip = False, widget=forms.Textarea(attrs={"class": "max-width-input"}))
    states = forms.CharField(label='Zustände', strip=False, widget=forms.TextInput(attrs={'size': '10'}))

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
    
class UpgmaNjForm (forms.Form):
    names = forms.CharField(label='Namen', required=False)
    csv_data = forms.CharField(
        label='CSV Data',
        widget=forms.Textarea(),
        initial="0;\t;\t;\t;\t;\n3;\t0;\t;\t;\t;\n7;\t8;\t0;\t;\t;\n9;\t10;\t10;\t0;\t;\n8;\t9;\t9;\t5;\t0;")
     
    def clean(self):
        cleaned_data = super().clean()
        csv_data = cleaned_data.get('csv_data')
        names = cleaned_data.get('names')

        rows = [row.strip().split(';') for row in csv_data.split('\n') if row.strip()]
        def parse(cell):
            try:
                 return float(cell)
            except ValueError or TypeError:
                 return None             
        cleaned_csv = [[parse(cell) for cell in row if parse(cell) is not None] for row in rows]
        if len(cleaned_csv[0]) == len(cleaned_csv):
            cleaned_csv = cleaned_csv[::-1]
            cleaned_csv = [row.reverse() for row in cleaned_csv]
        cleaned_csv = [[cell for cell in row[:i+1]] for i, row in enumerate(cleaned_csv)]
        cleaned_data['csv_data'] = cleaned_csv
        if names is None or names == '':
            def generate_names(num_columns):
                def convert_to_column_name(n):
                    result = []
                    while n:
                        n, remainder = divmod(n - 1, 26)
                        result.append(chr(65 + remainder))
                    return ''.join(result[::-1])
                
                column_names = [convert_to_column_name(i) for i in range(1, num_columns + 1)]
                return column_names
            cleaned_data['names'] = generate_names(len(cleaned_data['csv_data']))
        else:
            cleaned_data['names'] = [name.strip() for name in names.split(';') if name.strip() != '']
        return cleaned_data
    

    def is_valid(self):
        valid = super().is_valid()
        if valid:
            csv_data = self.cleaned_data.get('csv_data')
            names = self.cleaned_data.get('names')
            if len(names) != len(csv_data):
                self.add_error('names', "Die Anzahl von Namen sollte mit der Anzahl von Spalten/Zeilen übereinstimmen. Bitte geben Sie die Namen ein, separiert mit Semikolon oder lassen Sie das Eingabefeld frei, dann werden die Namen automatisch generiert")
                valid = False
            if len(csv_data) != len (csv_data[-1]):
                self.add_error('csv_data', "Die Anzahl der Zeilen soll gleich der Anzahl der Spalten sein") 
                valid = False  
            diag_is_valid = [row[-1] == 0.0 for row in csv_data]
            if False in diag_is_valid:
                self.add_error('csv_data', "Auf der Diagonale dürfen nur 0 stehen")
                valid = False
            count_is_valid = [len(row)==i+1 for i,row in enumerate(csv_data)]
            if False in count_is_valid:
                self.add_error('csv_data',"Die Matrix ist nicht diagonal oder nicht vollständig")
                valid = False
            if len(csv_data) < 2:
                self.add_error('csv_data',"Die Matrix soll aus mindestens zwei Zeilen bestehen")
                valid = False
        return valid
    
class SuffixArrayForm(forms.Form):
    sequence = forms.CharField(label='Text',widget=forms.Textarea(attrs={"class": "max-width-input"}), strip=False)
    pattern = forms.CharField(label='Muster', required=False, strip=False, widget=forms.TextInput(attrs={"class": "max-width-input"}))

    def is_valid(self):
        valid = super().is_valid()

        pattern = self.cleaned_data.get('pattern', '')
        sequence = self.cleaned_data.get('sequence', '')

        if len(pattern) > len(sequence):
                valid = False
                self.add_error('pattern', 'Pattern darf nicht länger als Sequenz sein')

        return valid 
    
class SuffixTreeTrieForm(forms.Form):
    sequence = forms.CharField(label='Text', widget=forms.TextInput(attrs={"class": "max-width-input"}))
    pattern = forms.CharField(label='Muster', required=False, widget=forms.TextInput(attrs={"class": "max-width-input"}))
    endchar = forms.CharField(label='Endzeichen', max_length=1, min_length=1, initial='$', widget=forms.TextInput(attrs={'size': '10'}))

    def is_valid(self):
        valid = super().is_valid()

        pattern = self.cleaned_data.get('pattern', '')
        sequence = self.cleaned_data.get('sequence', '')
        endchar = self.cleaned_data.get('endchar', '')
        if endchar in sequence:
            valid = False
            self.add_error('sequence', 'Endzeichen darf nicht im Text enthalten sein')
        if endchar in pattern:
            valid = False
            self.add_error('pattern', 'Endzeichen darf nicht im Muster enthalten sein')

        if len(pattern) > len(sequence):
            valid = False
            self.add_error('pattern', 'Pattern darf nicht länger als Sequenz sein')

        return valid 