from django.shortcuts import render
from .forms import ViterbiForm
from .lib import viterbi


def viterbi_view(request):
    form = ViterbiForm()
    if request.method == 'POST':
        form = ViterbiForm(request.POST)

        if form.is_valid():
            sequence = form.cleaned_data['sequence']
            states = form.cleaned_data['states']
            states.insert(0, 'Start')
            state_probabilities = []
            symbol_probabilities = []
            sum_is_valid = True
            state_input_values = request.POST.getlist('state_probabilities')
            symbol_input_values = request.POST.getlist('symbol_probabilities')         
            if len(state_input_values) == 0 or (len(state_input_values) != (len(states)-1)*len(states)):
                print('True')
                for state in states:
                    state_probabilities.append((state, [0.0] * (len(states)-1)))
            else:
                for i in range(len(states)):
                    start_position = i * (len(states) - 1)
                    values = [float(state_input_values[start_position + j]) for j in range(len(states) - 1)]
                    if sum(values) != 1:
                        sum_is_valid = True
                    state_probabilities.append((states[i], values))
            symbols = list(set(list(sequence)))

            if len(symbol_input_values) == 0 or (len(symbol_input_values) != (len(states)-1)*len(symbols)):
                for state in states:
                    if state != 'Start':
                        symbol_probabilities.append((state, [0.0] * len(symbols)))
            else:
                for i in range(len(states)-1):
                    start_position = i * (len(symbols) )
                    values = [float(symbol_input_values[start_position + j]) for j in range(len(symbols))]
                    if sum(values) != 1:
                        sum_is_valid = False
                    symbol_probabilities.append((states[i+1], values))
            if sum_is_valid:
                transition_matrix = state_probabilities.copy()
                transition_matrix.insert(0,(' ', states[1:]))
                emission_matrix = symbol_probabilities.copy()
                emission_matrix.insert(0,(' ', symbols))
                results = viterbi.get_results(sequence,transition_matrix,emission_matrix)
                context = {
                    'form': form,
                    'sequence': sequence,
                    'sum_is_valid' : sum_is_valid,
                    'probability_matrix_result' : results['probability'],
                    'log_probability_matrix_result' : results['log_probability'],
                    'path_matrix_result' : results['path_matrix'],
                    'path_max_value' : results['path'],
                    'path_log_max_value' : results['log_path'],
                    'states': states,
                    'state_probabilities': state_probabilities,
                    'symbols': symbols,
                    'symbol_probabilities': symbol_probabilities
                }
            else:
                context = {
                    'form': form,
                    'sequence': sequence,
                    'sum_is_valid' : sum_is_valid,
                    'states': states,
                    'state_probabilities': state_probabilities,
                    'symbols': symbols,
                    'symbol_probabilities': symbol_probabilities 
                    }
            return render(request, 'viterbi.html', context)

    return render(request, 'viterbi.html', {'form': form})
