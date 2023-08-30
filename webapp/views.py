from django.shortcuts import render
from .forms import *
from .lib import dotplot
from .lib import simple_search
from .lib import horspool
from .lib import overlap
from .lib import needleman_wunsch
from .lib import glocal_alignment
from .lib import viterbi
from .lib import smith_waterman
from .lib import upgma
from .lib import neighbour_joining

def horspool_view(request):
    form = HorspoolForm()  

    if request.method == 'POST':
        form = HorspoolForm(request.POST)

        if form.is_valid():
            pattern = form.cleaned_data['pattern']
            sequence = form.cleaned_data['sequence']
            selected_direction = form.cleaned_data['direction']
            backward = selected_direction == 'backward'
            results = horspool.get_result(pattern, sequence, backward)
            comparisons_count = results['comparisons_count']
            results_count = len(results['results'])
            file_content = f'Es wurden {comparisons_count} Vergleiche gemacht\nEs sind {results_count} Treffer an folgenden Positionen gefunden:\n'+' '.join(str(result) for result in results['results'])
            results = results['results'][:100]

            context = {
                'form': form,
                'results': results,
                'results_count' : results_count,
                'file_content': file_content,
                'comparisons_count' : comparisons_count
            }
            return render(request, 'horspool.html', context)

    context = {
        'form': form,
    }
    return render(request, 'horspool.html', context)


def simple_search_view(request):
    form = SimpleSearchForm()  

    if request.method == 'POST':
        form = SimpleSearchForm(request.POST)

        if form.is_valid():
            pattern = form.cleaned_data['pattern']
            sequence = form.cleaned_data['sequence']
            results = simple_search.get_result(pattern, sequence)
            comparisons_count = results['comparisons_count']
            results_count = len(results['results'])
            file_content = f'Es wurden {comparisons_count} Vergleiche gemacht\nEs sind {results_count} Treffer an folgenden Positionen gefunden:\n'+' '.join(str(result) for result in results['results'])
            results = results['results'][:100]

            context = {
                'form': form,
                'results': results,             
                'file_content': file_content, 
                'results_count' : results_count,             
                'comparisons_count' : comparisons_count
            }
            return render(request, 'simple_search.html', context)

    context = {
        'form': form,
    }
    return render(request, 'simple_search.html', context)

def dotplot_view(request):

    form = DotplotForm()

    if request.method == 'POST':
        form = DotplotForm(request.POST)

        if form.is_valid():
            seq1 = form.cleaned_data['sequence1']
            seq2 = form.cleaned_data['sequence2']
            result = dotplot.get_result(seq1, seq2)

            context = {
                'form': form,
                'results': result
            }

            return render(request, 'dotplot.html', context)

    context = {
        'form': form,
    }
    return render(request, 'dotplot.html', context)

def base_view(request):
    return render(request, 'base.html')

def needleman_wunsch_view(request):
    form = NeedlemanWunschForm()

    if request.method == 'POST':
        form = NeedlemanWunschForm(request.POST)

        if form.is_valid():
            seq1 = form.cleaned_data['sequence1']
            seq2 = form.cleaned_data['sequence2']
            match = form.cleaned_data['match']
            mismatch = form.cleaned_data['mismatch']
            gap_penalty = form.cleaned_data['gap_penalty']
            similarity = True if form.cleaned_data['optimization_field'] == 'similarity' else False
            result = needleman_wunsch.get_result(seq1, seq2, match, mismatch, gap_penalty, similarity) 

            if result is not None:
                result['traceback'] [0][0] = ''
                def create_fasta(alignments):
                    fasta_lines = []

                    for i, alignment in enumerate(alignments):
                        fasta_lines.append(f'>Alignment_{i + 1}')

                        for sequence in alignment['alignment']:
                            fasta_lines.append(sequence)

                    fasta_content = '\n'.join(fasta_lines)
                    return fasta_content

                fasta_content = create_fasta(result['alignments'])                
                context = {
                    'form': form,
                    'matrix': result['matrix'],
                    'alignments' : result['alignments'],
                    'score' : result['score'],
                    'traceback' : result['traceback'],
                    'fasta_content' : fasta_content
                }
            else:
                context = {
                    'form' : form,
                    'error' : True
                }
            return render(request, 'needleman_wunsch.html', context)
    context = {
        'form': form,
    }
    return render(request, 'needleman_wunsch.html',context)

def smith_waterman_view(request):
    form = SmithWatermanForm()

    if request.method == 'POST':
        form = SmithWatermanForm(request.POST)

        if form.is_valid():
            seq1 = form.cleaned_data['sequence1']
            seq2 = form.cleaned_data['sequence2']
            match = form.cleaned_data['match']
            mismatch = form.cleaned_data['mismatch']
            gap_penalty = form.cleaned_data['gap_penalty']
            result = smith_waterman.get_result(seq1, seq2, match, mismatch, gap_penalty)

            if result is not None:
                print(result)
                for sublist in result['traceback']:
                    for i in range(len(sublist)):
                        if sublist[i] is None:
                            sublist[i] = ''
                        elif isinstance(sublist[i], list) and None in sublist[i]:
                            sublist[i].remove(None)                
                context = {
                    'form': form,
                    'matrix': result['matrix'],
                    'alignments' : result['alignments'],
                    'score' : result['score'],
                    'traceback' : result['traceback']
                }
            else:
                context = {
                    'form' : form,
                    'error' : True
                }
            return render(request, 'smith_waterman.html', context)
    context = {
    'form': form,
}
    return render(request, 'smith_waterman.html', context)

def glocal_alignment_view(request):
    form = GlocalAlignmentForm()

    if request.method == 'POST':
        form = GlocalAlignmentForm(request.POST)

        if form.is_valid():
            seq1 = form.cleaned_data['sequence1']
            seq2 = form.cleaned_data['sequence2']
            match = form.cleaned_data['match']
            mismatch = form.cleaned_data['mismatch']
            threshold = form.cleaned_data['threshold']
            gap_penalty = form.cleaned_data['gap_penalty']
            similarity = True if form.cleaned_data['optimization_field'] == 'similarity' else False
            result = glocal_alignment.get_result(seq1, seq2, match, mismatch, gap_penalty, similarity, threshold)        

            if result is not None:                
                for sublist in result['traceback']:
                    for i in range(len(sublist)):
                        if sublist[i] is None:
                            sublist[i] = ''
                        elif isinstance(sublist[i], list) and None in sublist[i]:
                            sublist[i].remove(None)
                if len(result['alignments']) == 0:
                    pass
                    #result['alignments'] = [{'alignment':[], 'path':[]}]
                context = {
                    'form': form,
                    'matrix': result['matrix'],
                    'alignments' : result['alignments'],
                    'score' : result['score'],
                    'traceback' : result['traceback']
                }
            else:
                context = {
                    'form' : form,
                    'error' : True
                }
            return render(request, 'glocal_alignment.html', context)
    context = {
        'form': form,
    }
    return render(request, 'glocal_alignment.html', context)

def overlap_view(request):
    form = OverlapForm()

    if request.method == 'POST':
        form = OverlapForm(request.POST)

        if form.is_valid():
            seq1 = form.cleaned_data['sequence1']
            seq2 = form.cleaned_data['sequence2']
            match = form.cleaned_data['match']
            mismatch = form.cleaned_data['mismatch']
            gap_penalty = form.cleaned_data['gap_penalty']

            similarity = True if form.cleaned_data['optimization_field'] == 'similarity' else False
            result = overlap.get_result(seq1, seq2, match, mismatch, gap_penalty, similarity)         
            
            if result is not None:
                print (result)
                for sublist in result['traceback']:
                    for i in range(len(sublist)):
                        if sublist[i] is None:
                            sublist[i] = ''
                        elif isinstance(sublist[i], list) and None in sublist[i]:
                            sublist[i].remove(None)                 
                context = {
                    'form': form,
                    'matrix': result['matrix'],
                    'alignments' : result['alignments'],
                    'score' : result['score'],
                    'traceback' : result['traceback']
                }
            else:
                context = {
                    'form' : form,
                    'error' : True
                }
            return render(request, 'overlap.html', context)
    context = {
        'form': form,
    }
    return render(request, 'overlap.html', context)

def upgma_view(request):
    form = UpgmaNjForm()
    if request.method == 'POST':
        form = UpgmaNjForm(request.POST)
        if form.is_valid():
            csv_data = form.cleaned_data['csv_data']
            names = form.cleaned_data['names']
            
            result = upgma.get_results(names, csv_data)
            if result is not None:
                context = {
                    'form': form,
                    'newick' : result['newick'],
                    'base64_plot' : result['base64_plot'],
                    'iterations' : result['intermatrixes']
                } 

                return render(request, 'upgma.html', context)
    context = {
        'form': form,
    }
    return render(request, 'upgma.html', context)

def neighbour_joining_view(request):
    form = UpgmaNjForm()
    if request.method == 'POST':
        form = UpgmaNjForm(request.POST)
        if form.is_valid():
            csv_data = form.cleaned_data['csv_data']
            names = form.cleaned_data['names']
            result = neighbour_joining.get_results(names, csv_data)
            print(result['intermatrixes'])
            if result is not None:
                context = {
                    'form': form,
                    'newick' : result['newick'],
                    'base64_plot' : result['base64_plot'],
                    'iterations' : result['intermatrixes']
                } 
                return render(request, 'neighbour_joining.html', context)
    context = {
        'form': form,
    }
    return render(request, 'neighbour_joining.html', context)

def suffix_tree_view(request):
    return render(request, 'suffix_tree.html')    

def suffix_trie_view(request):
    return render(request, 'suffix_trie.html')  

def suffix_array_view(request):
    return render(request, 'suffix_array.html')      

def homepage_view(request):
    return render(request, 'homepage.html') 

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
                sum_is_valid = False
                for state in states:
                    state_probabilities.append((state, [0.0] * (len(states)-1)))
            else:
                for i in range(len(states)):
                    start_position = i * (len(states) - 1)
                    values = [float(state_input_values[start_position + j]) for j in range(len(states) - 1)]
                    if sum(values) != 1:
                        sum_is_valid = False
                    state_probabilities.append((states[i], values))
            symbols = list(set(list(sequence)))

            if len(symbol_input_values) == 0 or (len(symbol_input_values) != (len(states)-1)*len(symbols)):
                sum_is_valid = False
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
                    'paths' : results['states'],
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
