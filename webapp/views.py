from django.shortcuts import render
from .forms import DotplotForm
from .lib import dotplot

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


