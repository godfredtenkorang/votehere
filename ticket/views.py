from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import HttpRequest, JsonResponse
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


def verify_ticket_qr(request, verification_token):
    try:
        ticket = TicketPayment.objects.get(qr_verification_token=verification_token)
    except TicketPayment.DoesNotExist:
        
        return JsonResponse({
            'status': 'error', 
            'message': 'Invalid ticket QR code'
            }, status=404)

    # Verify the QR code
    result = ticket.verify_qr_code()
    
    if result == "already_scanned":
        return JsonResponse({
            'status': 'already_scanned', 
            'message': 'This ticket has already been scanned.',
            'ticket_info': {
                'event': ticket.event.name,
                'ticket_type': ticket.ticket_type.name,
                'quantity': ticket.quantity,
                'qr_verification_date': ticket.qr_verification_date.isoformat() if ticket.qr_verification_date else None,
            }
            })
    elif result == "verified":
        return JsonResponse({
            'status': 'verified', 
            'message': 'Ticket verified successfully.',
            'ticket_info': {
                'event': ticket.event.name,
                'ticket_type': ticket.ticket_type.name,
                'quantity': ticket.quantity,
                'qr_verification_date': ticket.qr_verification_date.isoformat(),
            }
            })
    return JsonResponse({
        'status': 'error', 
        'message': 'An error occurred during verification.'
        }, status=500)
    

def ticket_verification_page(request):
    """Page for event staff to manually verify tickets"""
    if request.method == 'POST':
        verification_token = request.POST.get('verification_token')
        try:
            ticket = TicketPayment.objects.get(qr_verification_token=verification_token)
            result = ticket.verify_qr_code()
            if result == "already_scanned":
                messages.warning(request, f"This ticket has already scanned on {ticket.qr_verification_date}.")
            elif result == "verified":
                messages.success(request, f"Ticket verified successfully for {ticket.event.name}.")
            return render(request, 'ticket/verification_result.html', {'ticket': ticket, 'result': result})
        except TicketPayment.DoesNotExist:
            messages.error(request, "Invalid ticket QR code.")
    return render(request, 'ticket/ticket_verification.html')


def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    ticket = get_object_or_404(TicketPayment, ref=ref)
    
    # Case 1: Payment already verified (prevent duplicate processing)
    if ticket.verified:
        messages.info(request, "This payment was already processed. Tickets were not added again.")
        return render(request, 'ticket/ticket_success.html')

    
    verified = ticket.verify_payment()

    if verified:
        try:
            # Update available ticket
            event = ticket.ticket_type
            event.available_tickets -= ticket.quantity
            event.save()
            
            # Generate QR code if not already generated
            if not ticket.qr_code:
                ticket.generate_qr_code()
            
            
            # Send email with QR code
            subject = f"Your Ticket for {event.event.name}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [ticket.email]
            
            html_content = render_to_string('ticket/ticket_email.html', {'ticket': ticket, 'event': event})
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            messages.success(request, 'Payment successful! Your ticket has been confirmed.')
            return render(request, 'ticket/ticket_success.html')
        except Exception as e:
            messages.error(request, f"Error processing payment: {e}")
            return render(request, 'ticket/ticket_failed.html')
    else:
        messages.error(request, "Payment verification failed.")
        return render(request, 'ticket/ticket_failed.html')
    
def ticket_success(request):
    context = {
        'title': 'Ticket success',
    }
    return render(request, 'ticket/ticket_success.html', context)

def ticket_failed(request):
    context = {
        'title': 'Ticket failed',
    }
    return render(request, 'ticket/ticket_failed.html', context)
