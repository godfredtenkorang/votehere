from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import HttpRequest
from .models import Event, TicketPayment, TicketType
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
        ticket_type_id = request.POST.get('ticket_type')
        try:
            ticket_type = TicketType.objects.get(id=ticket_type_id, event=event)
        except TicketType.DoesNotExist:
            messages.error(request, "Invalid ticket type selected.")
            return redirect('ticketForm', event_slug=event.slug)
            
        if quantity > ticket_type.available_tickets:
            messages.error(request, f"Only {ticket_type.available_tickets} tickets available for {ticket_type.name}.")
            return redirect('ticketForm', event_slug=event.slug)
            
        amount = int(ticket_type.price * quantity)
        

        ticket = TicketPayment(
            event=event,
            ticket_type=ticket_type,
            phone=phone,
            email=email,
            quantity=quantity,
            amount=amount,
        )
        ticket.save()
        
        return render(request, 'ticket/make_payment.html', {'ticket': ticket, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})

        
       
    
    context = {
        'event': event,
        'title': 'Events'
    }
    return render(request, 'ticket/ticketForm.html', context)


def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    ticket = get_object_or_404(TicketPayment, ref=ref)
    
    # Case 1: Payment already verified (prevent duplicate processing)
    if ticket.verified:
        messages.info(request, "This payment was already processed. Votes were not added again.")
        return redirect('ticketForm', event_slug=ticket.event.slug)

    
    verified = ticket.verify_payment()

    if verified:
        try:
            event = ticket.ticket_type
            event.available_tickets -= ticket.quantity
            event.save()
            
            subject = f"Your Ticket for {event.event.name}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [ticket.email]
            
            html_content = render_to_string('ticket/ticket_email.html', {'ticket': ticket, 'event': event})
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            messages.success(request, 'Payment successful! Your ticket has been confirmed.')
            return redirect('ticketForm', event_slug=ticket.event.slug)
        except Exception as e:
            messages.error(request, f"Error processing payment: {e}")
            return redirect('ticketForm', event_slug=ticket.event.slug)
    else:
        messages.error(request, "Payment verification failed.")
        return redirect('ticketForm', event_slug=ticket.event.slug)
    
