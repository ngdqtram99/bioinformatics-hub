from django.shortcuts import render

from .forms import HorspoolForm
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
                'file_content': file_content,
                'comparsions_count' : comparsions_count
            }
            return render(request, 'horspool.html', context)

    context = {
        'form': form,
    }
    return render(request, 'horspool.html', context)