from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import DonationCause, DonationPayment
from django.contrib import messages
from django.conf import settings
from .utils import send_sms_to_donor

# Create your views here.
def donation_page(request):
    donation = DonationCause.objects.all().order_by('-date_added')
    
    context = {
        'donation_causes': donation,
        'title': 'Donation Page'
    }
    """
    Render the donation page.
    """
    return render(request, 'donation/donation_page.html', context)


def donation_detail(request:HttpRequest, donation_slug) -> HttpResponse:
    """
    Render the detail page for a specific donation cause.
    """
    donation = DonationCause.objects.get(slug=donation_slug)
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        amount = request.POST['amount']
        amount = int(amount)  # Ensure amount is an integer
        donation = DonationPayment(donation=donation, name=name, phone=phone, email=email, amount=amount)
        donation.save()
        return render(request, 'donation/make_payment.html', {'donation': donation, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})

    
    context = {
        'donation': donation,
        'title': f'Donation Detail - {donation.name}'
    }
    
    return render(request, 'donation/donation_detail.html', context)

def make_payment(request):
    return render(request, 'donation/make_payment.html')

def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(DonationPayment, ref=ref)
    
    verified = payment.verify_payment()
    if verified:
        donation = payment.donation
        donation.current_amount += payment.amount
        donation.save()
        payment.verified = True
        payment.save()
        send_sms_to_donor(
            phone=payment.phone,
            name=payment.name,
            amount=payment.amount,
            donation=donation.name
        )
        messages.success(request, "Payment verified successfully! Thank you for your donation.")
        return redirect('donation_detail', donation_slug=payment.donation.slug)
    else:
        messages.error(request, "Payment verification failed. Please try again.")
        return redirect('donation_detail', donation_slug=payment.donation.slug)