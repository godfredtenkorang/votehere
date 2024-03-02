from django.shortcuts import render, get_object_or_404
from vote.models import Nominees

# Create your views here.
def make_payment(request):
    return render(request, 'payment/make_payment.html')


def result(request):
    return render(request, 'payment/resultPage.html')


def nominees(request, nominee_slug):
    nominee = get_object_or_404(Nominees, slug=nominee_slug)
    context = {
        'nominee': nominee,
    }
    return render(request, 'payment/nomineesPage.html', context)
