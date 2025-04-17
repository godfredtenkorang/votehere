from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import HttpRequest
from .models import Event, TicketPayment
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from paystackapi.transaction import Transaction
import random
import string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def ticketing(request):
    events = Event.objects.all()
    context = {
        'events': events,
        'title': 'Events'
    }
    return render(request, 'ticket/ticketting.html', context)


def purchase_ticket(request: HttpRequest, event_slug) -> HttpResponse:
    event = get_object_or_404(Event, slug=event_slug)
    if request.method == 'POST':
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        quantity = int(request.POST.get('quantity', 1))
        if quantity > event.available_tickets:
            messages.error(request, "Not enough tickets available.")
            return redirect('ticketForm', event_slug=event.slug)
        amount = int(event.price * quantity)
       
        tickets = TicketPayment(
            event=event,
            phone=phone,
            email=email,
            quantity=quantity,
            amount=amount,
        )
        tickets.save()
        
        return render(request, 'ticket/make_payment.html', {'ticket': tickets, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})

        
       
    
    context = {
        'event': event,
        'title': 'Events'
    }
    return render(request, 'ticket/ticketForm.html', context)


def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    ticket = get_object_or_404(TicketPayment, ref=ref)
    
    verified = ticket.verify_payment()

    if verified:

        event = ticket.event
        event.available_tickets -= ticket.quantity
        event.save()
        
    
        messages.success(request, 'Payment successful! Your ticket has been confirmed.')
        return redirect('ticketForm', event_slug=ticket.event.slug)
    
    else:
        messages.error(request, "Payment verification failed.")
        return redirect('ticketForm', event_slug=ticket.event.slug)
    
