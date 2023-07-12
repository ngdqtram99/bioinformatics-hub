from django import forms

class ViterbiForm(forms.Form):
    sequence = forms.CharField(label='Sequenz')
    states = forms.CharField(label='Zustände')

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
                if len(states.split(';')) > 10 or len(states.split(';')) < 2:
                    self.add_error('states', "Geben Sie nicht mehr als 10  und nicht weniger als 2 Zustände ein")
                    valid = False
        return valid