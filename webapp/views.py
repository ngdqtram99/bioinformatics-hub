from django.shortcuts import render
from .forms import DotplotForm
from .forms import SimpleSearchForm
from .forms import HorspoolForm
from .lib import dotplot
from .lib import simple_search
from .lib import horspool

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
            comparsions_count = results['comparsions_count']
            results_count = len(results['results'])
            file_content = f'Es wurden {comparsions_count} Vergleiche gemacht\nEs sind {results_count} Treffer an folgenden Positionen gefunden:\n'+' '.join(str(result) for result in results['results'])
            results = results['results'][:100]

            context = {
                'form': form,
                'results': results,
                'results_count' : results_count,
                'file_content': file_content,
                'comparsions_count' : comparsions_count
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
            comparsions_count = results['comparsions_count']
            results_count = len(results['results'])
            file_content = f'Es wurden {comparsions_count} Vergleiche gemacht\nEs sind {results_count} Treffer an folgenden Positionen gefunden:\n'+' '.join(str(result) for result in results['results'])
            results = results['results'][:100]

            context = {
                'form': form,
                'results': results,             
                'file_content': file_content, 
                'results_count' : results_count,             
                'comparsions_count' : comparsions_count
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
