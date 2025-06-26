from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from payment.models import Payment, Nominees
from ussd.models import PaymentTransaction
from vote.models import SubCategory, Category
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.conf import settings
from . import forms
from django.utils import timezone
from .models import PageExpiration
from .utils import send_sms_to_voter, send_sms_to_nominee_for_vote
from django.db.models import Q  # New

# Create your views here.
def make_payment(request):
    return render(request, 'payment/make_payment.html')


def result(request, result_slug):
    sub_category = get_object_or_404(SubCategory, slug=result_slug)
    
    # If sub_category allows checking results without access code
    if sub_category.can_check_result:
        # Get all nominees for this sub_category ordered by votes
        nominees = Nominees.objects.filter(sub_category=sub_category).order_by('-total_vote')
        context = {
            'sub_category': sub_category,
            'nominees': nominees,
            'title': 'Results',
            'show_result': True,
            'public_results': True  # Add this flag to differentiate in template
        }
        return render(request, 'payment/resultPage.html', context)

    
    if request.method == 'POST':
        access_code = request.POST.get('access_code', '').strip()
        try:
            nominee = Nominees.objects.get(sub_category=sub_category, access_code=access_code)
            context = {
                'sub_category': sub_category,
                'nominee': nominee,
                'title': 'Your Result',
                'show_result': True,
                'public_results': False
            }
            return render(request, 'payment/resultPage.html', context)
        except Nominees.DoesNotExist:
            messages.error(request, 'Invalid access code.')
            return redirect('result', result_slug=result_slug)
    # sub_category = None
    # results = Nominees.objects.all()
    # if result_slug:
    #     sub_category = get_object_or_404(SubCategory, slug=result_slug)
    #     results = results.filter(sub_category=sub_category)
    # results = get_object_or_404(Nominees, slug=result_slug)
    
    context = {
        'sub_category': sub_category,
        'title': 'Enter Access Code',
        'show_result': False
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
    search_item = request.GET.get('search')
    sub_category = None
    nominees = Nominees.objects.all()
    current_time = timezone.now()
    if nominee_slug:
        sub_category = get_object_or_404(SubCategory, slug=nominee_slug)
        nominees = nominees.filter(sub_category=sub_category)
    
    # Add search functionality
    if search_item:
        nominees = nominees.filter(
            Q(name__icontains=search_item)
        )
    context = {
        'sub_category': sub_category,
        'nominees': nominees,
        'current_time': current_time,
        'title': 'Nominees',
        'search_item': search_item,
    }
    return render(request, 'payment/nomineesPage.html', context)


def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    
    # Case 1: Payment already verified (prevent duplicate processing)
    if payment.verified:
        messages.info(request, "This payment was already processed. Votes were not added again.")
        return render(request, 'payment/vote_success.html')

    verified = payment.verify_payment()
    if verified:
        try:
            nominee_obj = payment.nominee
            nominee_obj.total_vote += payment.vote
            nominee_obj.save()
            payment.verified = True
            payment.save()
            send_sms_to_voter(phone_number=payment.phone, name=payment.nominee.name, category=payment.content, amount=payment.total_amount, transaction_id=payment.transaction_id)
            send_sms_to_nominee_for_vote(phone_number=payment.nominee.phone_number, name=payment.nominee.name, vote=payment.vote, phone=payment.phone, transaction_id=payment.transaction_id)
            messages.success(request, "Payment verified successfully! Votes added.")
            return render(request, 'payment/vote_success.html')
        except Exception as e:
            messages.error(request, f"Error processing payment: {e}")
            return render(request, 'payment/vote_failed.html')
    else:
        messages.error(request, "Payment verification failed. Please try again.")
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


def search_transaction(request):
    transaction_id = request.GET.get('transaction_id', '').strip()
    payment = None
    
    if transaction_id:
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            pass
    
    ussd_transaction_id = request.GET.get('ussd_transaction_id', '').strip().upper()
    transaction = None
    
    if ussd_transaction_id:
        try:
            transaction = PaymentTransaction.objects.get(transaction_id=ussd_transaction_id)
        except PaymentTransaction.DoesNotExist:
            pass
        
    return render(request, 'payment/search_transaction.html', {
        'payment': payment,
        'transaction_id': transaction_id,
        'transaction': transaction,
        'ussd_transaction_id': ussd_transaction_id
    })
    



def access_denied(request):
    return render(request, 'payment/access_denied.html')