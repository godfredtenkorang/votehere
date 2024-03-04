from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from payment.models import Payment
from vote.models import Nominees
from django.http import HttpRequest
from django.contrib import messages
from django.conf import settings

# Create your views here.
def make_payment(request):
    return render(request, 'payment/make_payment.html')


def result(request):
    return render(request, 'payment/resultPage.html')


def nominees(request: HttpRequest, nominee_slug) -> HttpResponse:
    nominee = get_object_or_404(Nominees, slug=nominee_slug)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        vote = request.POST['vote']
        votes = Payment(name=name, email=email, phone=phone, vote=vote)
        payment = votes.save()
        return render(request, 'payment/make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    context = {
        'nominee': nominee,
    }
    return render(request, 'payment/nomineesPage.html', context)


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification Successful')
    else:
        messages.error(request, 'Verification Failed')
    return redirect('nominee_detail')
