from django.shortcuts import render
from .forms import *
from .lib import dotplot
from .lib import simple_search
from .lib import horspool
from .lib import overlap

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
            #result = needleman_wunsch.get_result(seq1, seq2, match, mismatch, gap_penalty, similarity)
            result={} 
            result['matrix'] = [ #nur zum Schauen/Testen
          [0, -10, -20, -30, -40],
          [-10, 1, -9, -19, -29],
          [-20, -9, 2, -8, -18],
          [-30, -19, -8, 1, -9],
          [-40, -29, -18, -7, 0],
          [-50,-39,-28,-17,-6]
        ]  
            result['alignments']=[{'alignment':['AATCG', '||:||', 'AA-CG'],
                                   'path':[
                                    [[5, 4], 'diag'],
                                    [[4, 3], 'diag'],
                                    [[3, 2], 'vert'],
                                    [[2, 2], 'diag'],
                                    [[1, 1], 'diag'],
                                    [[0, 0]]]},
                                    {'alignment':['AATCG', '|::||', 'A-ACG'],
                                   'path':[
                                    [[5, 4], 'diag'],
                                    [[4, 3], 'diag'],
                                    [[3, 2], 'hor'],
                                    [[3, 1], 'diag'],
                                    [[2, 0], 'vert'],
                                    [[1, 0], 'vert'],
                                    [[0, 0]]]}]
            
            if result is not None:

                context = {
                    'form': form,
                    'matrix': result['matrix'],
                    'alignments' : result['alignments'],
                    #'alignments' : result['alignments'],
                    'score' : 4
                }
                print(context)
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
    return render(request, 'smith_waterman.html')

def glocal_alignment_view(request):
    return render(request, 'glocal_alignment.html')

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
            result = overlap.get_result(seq1, seq2, match, mismatch, gap_penalty)
            if result is not None:

                context = {
                    'form': form,
                    'matrix': result['matrix'],
                    'alignments' : result['alignments'],
                    'score' : result['score']
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
    return render(request, 'upgma.html')

def neighbour_joining_view(request):
    return render(request, 'neighbour_joining.html')

def suffix_tree_view(request):
    return render(request, 'suffix_tree.html')    

def suffix_trie_view(request):
    return render(request, 'suffix_trie.html')  

def suffix_array_view(request):
    return render(request, 'suffix_array.html')      

def homepage_view(request):
    return render(request, 'homepage.html') 