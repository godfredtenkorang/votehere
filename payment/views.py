from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from payment.models import Payment, Nominees
from vote.models import SubCategory, Category
from django.http import HttpRequest, HttpResponseForbidden
from django.contrib import messages
from django.conf import settings
from . import forms
from django.utils import timezone
from .models import PageExpiration

# Create your views here.
def make_payment(request):
    return render(request, 'payment/make_payment.html')


def result(request, result_slug):
    sub_category = None
    results = Nominees.objects.all()
    if result_slug:
        sub_category = get_object_or_404(SubCategory, slug=result_slug)
        results = results.filter(sub_category=sub_category)
    # results = get_object_or_404(Nominees, slug=result_slug)
    
    context = {
        'sub_category': sub_category,
        'results': results,
        'title': 'Results'
    }
    
    return render(request, 'payment/resultPage.html', context)



# def nominees(request, nominee_slug):
#     nominee = get_object_or_404(Nominees, slug=nominee_slug)

#     context = {
#         'nominee': nominee,
#     }
#     return render(request, 'payment/nomineesPage.html', context)



def vote(request: HttpRequest, nominee_slug) -> HttpResponse:
    nominee = get_object_or_404(Nominees, slug=nominee_slug)
    
    if nominee.is_due():
        return render(request, 'payment/access_denied.html')
    
    if request.method == 'POST':
        category = nominee.category
        phone = request.POST['phone']
        vote = request.POST['vote']
        amount = request.POST['amount']
        total_amount = request.POST['total_amount']
        payment = Payment(category=category, nominee=nominee, content=nominee.sub_category, phone=phone, vote=vote, amount=amount, total_amount=total_amount)
        payment.save()
        return render(request, 'payment/make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})



    context = {
        'title': 'Vote',
        'nominee': nominee,
    }
    return render(request, 'payment/vote.html', context)


def nominees(request, nominee_slug):
    sub_category = None
    nominees = Nominees.objects.all()
    current_time = timezone.now()
    if nominee_slug:
        sub_category = get_object_or_404(SubCategory, slug=nominee_slug)
        nominees = nominees.filter(sub_category=sub_category)
    
    
    context = {
        'sub_category': sub_category,
        'nominees': nominees,
        'current_time': current_time,
        'title': 'Nominees',
    }
    return render(request, 'payment/nomineesPage.html', context)


def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        nominee_obj = payment.nominee
        nominee_obj.total_vote += payment.vote
        nominee_obj.save()
        return render(request, 'payment/vote_success.html')
    else:
        return render(request, 'payment/vote_failed.html')
    
    

def vote_success(request):
    context = {
        'title': 'Vote success',
    }
    return render(request, 'payment/vote_success.html', context)

def vote_failed(request):
    context = {
        'title': 'Vote failed',
    }
    return render(request, 'payment/vote_failed.html', context)


def access_denied(request):
    return render(request, 'payment/access_denied.html')