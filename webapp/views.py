from django.shortcuts import render

from .forms import SimpleSearchForm
from .lib import simple_search

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