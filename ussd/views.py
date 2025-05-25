import hashlib
import hmac
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomSession, PaymentTransaction
import json
from hashlib import md5
import uuid
import requests
from decimal import Decimal
import random
from django.conf import settings
from payment.models import Nominees
from ticket.models import Event, TicketType
from datetime import datetime
from django.utils import timezone
from ticket.utis import send_ticket_sms
from .utils import send_sms_to_voter, send_sms_to_nominee_for_vote



from django.views import View



def generate_random_key():
    return random.randint(1000, 9999)

# Main USSD API view
@csrf_exempt
def ussd_api(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        # Extracting request data
        user_id = data.get('USERID')
        msisdn = data.get('MSISDN')
         # Ensure MSISDN starts with 233
        if msisdn.startswith("0"):  # If it starts with 0, replace it
            msisdn = "233" + msisdn[1:]
        elif not msisdn.startswith("233"):  # If it doesn’t start with 233, ensure proper format
            msisdn = "233" + msisdn
            
        user_data = data.get('USERDATA', '').strip().upper()
        msgtype = data.get('MSGTYPE')  # Determines if initial request (True) or follow-up (False)
        network = data.get('NETWORK')

        # Function to generate response
        def send_response(msg, msgtype=True):
            return {
                'USERID': user_id,
                'MSISDN': msisdn,
                'MSG': msg,
                'MSGTYPE': msgtype
            }

        # Check user ID
        if user_id == 'GODEY100':
            # Generate session key using hashed MSISDN
            session_key = md5(msisdn.encode('utf-8')).hexdigest()
            
            session, created = CustomSession.objects.get_or_create(session_key=session_key, defaults={'user_id': user_id})
            
            # Check if session is expired (except for new sessions)
            if not created and session.is_expired:
                session.delete()
                return JsonResponse(send_response("Session expired. Please start again.", False))
            # Update last activity for every request
            session.last_activity = timezone.now()
            
            if msgtype:  # Initial request
                session.level = 'start'
                session.save()
                message = "Welcome to VoteAfric.\n1. Voting\n2. Ticketing\nContact: 0553912334\nor: 0558156844"
                return JsonResponse(send_response(message, True))
            else:
                session.last_activity = timezone.now() # Follow-up request
                session.save()
                level = session.level
                if level == 'start':
                    if user_data == '1': # Voting
                        session.payment_type = 'VOTE'
                        session.level = 'vote_start'
                        session.save()
                        message = "Enter Nominee's code"
                        return JsonResponse(send_response(message, True))
                    elif user_data == '2': # Ticketing
                        session.payment_type = 'TICKET'
                        session.level = 'ticket_start'
                        session.save()
                        message = "Enter Event code"
                        return JsonResponse(send_response(message, True))
                    else:
                        session.delete()
                        return JsonResponse(send_response("Invalid option. Please try again.", False))
                    
                # Voting flow
                elif level == 'vote_start':
                    try:
                        nominee = Nominees.objects.get(code__iexact=user_data)
                        
                        # Get category information
                        # category_name = nominee.category.award if nominee.category else "General"
                        
                        # check if voting has ended for this nominee
                        if timezone.now() > nominee.end_date:
                            session.delete()
                            return JsonResponse(send_response("Voting has ended.", False))
                        message = (
                            f"Confirm Candidate\n"
                            f"Name: {nominee.name}\n"
                            f"Category: {nominee.sub_category}\n"
                            f"1) Confirm\n2) Cancel"
                        )
                        session.candidate_id = nominee.code
                        session.level = 'voting_confirm'
                        session.save()
                        return JsonResponse(send_response(message, True))
                    
                    except Nominees.DoesNotExist:
                        session.delete()
                        return JsonResponse(send_response("Invalid nominee code. Please try again.", False))

                elif level == 'voting_confirm':
                    if user_data == '1':
                        nominee = Nominees.objects.get(code__iexact=session.candidate_id)
                        price_per_vote = nominee.price_per_vote
                        session.level = 'votes'
                        session.save()
                        message = f"Enter the number of votes. \n\n A vote is GH¢{price_per_vote}."
                        return JsonResponse(send_response(message, True))
                    elif user_data == '2':
                        session.delete()
                        return JsonResponse(send_response("You have cancelled the process.", False))
                    else:
                        session.delete()
                        return JsonResponse(send_response("Invalid input. Please try again.", False))

                elif level == 'votes':
                    try:
                        votes = int(user_data)
                        nominee = Nominees.objects.get(code__iexact=session.candidate_id)
                        price_per_vote = nominee.price_per_vote
                    except ValueError:
                        session.delete()
                        return JsonResponse(send_response("Invalid number of votes entered. Please try again.", False))
                    except Nominees.DoesNotExist:
                        session.delete()
                        return JsonResponse(send_response("Nominee not found.", False))
                    
                    session.level = 'vote_payment'
                    session.votes = votes
                    session.amount = Decimal(votes) * Decimal(price_per_vote)
                    session.save()
                    message = f"You have entered {votes} votes \nTotal amount is GH¢{float(session.amount):.2f}.\n\nPress 1 to proceed."
                    return JsonResponse(send_response(message, True))
                
                # Ticketing flow
                elif level == 'ticket_start':
                    try:
                        event = Event.objects.get(code__iexact=user_data)
                        if timezone.now() > event.end_date:
                            session.delete()
                            return JsonResponse(send_response("Event has ended.", False))
                        if event.available_tickets <= 0:
                            session.delete()
                            return JsonResponse(send_response("Tickets are sold out.", False))
                        # Build ticket type options
                        ticket_options = "\n".join(
                            [f"{i+1}) {t.name} - GH¢{t.price:.2f}" 
                            for i, t in enumerate(event.ticket_types.all())]
                        )
                        message = (
                            f"Select Ticket Type:\n"
                            f"{ticket_options}\n"
                            f"0) Cancel"
                        )
                        # message = (
                        #     f"Confirm Event\n"
                        #     f"Name: {event.name}\n"
                        #     f"Price per ticket: GH¢{event.price:.2f}\n"
                        #     f"Available tickets: {event.available_tickets}\n"
                        #     f"1) Confirm\n"
                        #     f"2) Cancel"
                        # )
                        session.event_id = event.code
                        session.level = 'ticket_type_select'
                        session.save()
                        return JsonResponse(send_response(message, True))
                    
                    except Event.DoesNotExist:
                        return JsonResponse(send_response('Invalid event code. Please try again.', False))
                    except Exception as e:
                        print(f"Error processing event code: {str(e)}")  # For debugging
                        return JsonResponse(send_response("System error. Please try again later.", False))
                
                elif level == 'ticket_type_select':
                    try:
                        option = int(user_data)
                        if option == 0:
                            session.delete()
                            return JsonResponse(send_response("You have cancelled the process.", False))
                            
                        ticket_types = list(Event.objects.get(code=session.event_id).ticket_types.all())
                        selected_type = ticket_types[option-1]
                        
                        session.ticket_type_id = selected_type.id
                        session.level = 'ticket_quantity'
                        session.save()
                        
                        message = f"Enter number of tickets (1-{selected_type.available_tickets})"
                        return JsonResponse(send_response(message, True))
                        
                    except (ValueError, IndexError):
                        session.delete()
                        return JsonResponse(send_response("Invalid option selected. Please try again.", False))

                elif level == 'ticket_quantity':
                    try:
                        tickets = int(user_data)
                        ticket_type = TicketType.objects.get(id=session.ticket_type_id, event__code=session.event_id)
                        
                        if tickets <= 0:
                            session.delete()
                            return JsonResponse(send_response("Invalid number of tickets. Please try again.", False))
                        if tickets > ticket_type.available_tickets:
                            session.delete()
                            return JsonResponse(send_response(f"Only {ticket_type.available_tickets} tickets available. Please enter a lower number.", False))
                    except ValueError:
                        session.delete()
                        return JsonResponse(send_response("Invalid number of tickets entered. Please try again.", False))
                    except TicketType.DoesNotExist:
                        session.delete()
                        return JsonResponse(send_response("Invalid ticket selection. Please start over.", False))
                    
                    session.tickets = tickets
                    session.amount = Decimal(tickets) * ticket_type.price
                    session.level = 'ticket_payment'
                    session.save()
                    message = f"You have selected {ticket_type.name} tickets\nQuantity: {tickets}\nTotal amount is GH¢{float(session.amount):.2f}.\n\nPress 1 to proceed."
                    return JsonResponse(send_response(message, True))

                
                elif level.endswith('_payment'):
                    if user_data != '1':
                        session.delete()
                        return JsonResponse(send_response('Transaction cancelled.', False))
                    

                    amount = session.amount
                    endpoint = "https://api.nalosolutions.com/payplus/api/"
                    telephone = msisdn
                    network_type = network
                    username = 'votfric_gen'
                    # password = 'bVdwy86yoWtdZcW'
                    password = 'Nrkl)CYr'
                    merchant_id = 'NPS_000288'
                    key = str(generate_random_key())
                    hashed_password = md5(password.encode()).hexdigest()
                    concat_keys = f"{username}{key}{hashed_password}"
                    secrete = md5(concat_keys.encode()).hexdigest()
                    callback = 'https://voteafric.com/ussd/webhooks/callback/'
                    item_desc = 'Payment for vote'
                    # Determine payment description based on type
                    if session.payment_type == 'VOTE':
                        item_desc = f"Votes for {session.candidate_id}"
                    elif session.payment_type == 'TICKET':
                        item_desc = f"Tickets for {session.event_id}"
                    order_id = str(uuid.uuid4())
                    session.order_id = order_id
                    session.msisdn = msisdn
                    session.save()
                    
                    if network_type.upper() == 'VODAFONE':
                        payload = {
                            'merchant_id': merchant_id,
                            'secrete': secrete,
                            'key': key,
                            'order_id': order_id,
                            'customerName': str(telephone),
                            'amount': str(amount),
                            'item_desc': item_desc,
                            'customerNumber': str(telephone),
                            'payby': 'VODAFONE',
                            'newVodaPayment': True,  # This is specific to Vodafone
                            'callback': callback
                        }
                    # secrete = f"{secrete[:4]} {secrete[4:]}"
                    else:
                    # Payment payload
                        payload = {
                            'payby': str(network_type),
                            'order_id': order_id,
                            'customerNumber': str(telephone),
                            'customerName': str(telephone),
                            'isussd': 1,
                            'amount': str(amount),
                            'merchant_id': merchant_id,
                            'secrete': secrete,
                            'key': key,
                            'callback': callback,
                            'item_desc': item_desc,

                
                        }

                    headers = {
                        "Content-Type": "application/json",
                    }

                    try:
                        
                    # Sending payment request
                        response = requests.post(endpoint, json=payload, headers=headers)
                        print(response)
                
                    
                    
                        if response.status_code == 200:
                            session.save()
                            # print(secrete_full)
                            print(hashed_password)
                            print(concat_keys)
                            print(secrete)
                            print(key)
                            message = (
                                f"You are about to pay GH¢{amount:.2f}. "
                                f"Please approve the payment prompt on your phone."
                            )
                            return JsonResponse(send_response(message, False))
                            
                            
                        else:
                            session.delete()
                            error_msg = response.json().get('message', 'Payment request failed')
                            return JsonResponse(send_response(f"Payment failed: {error_msg}. Please try again.", False))
                    except requests.exceptions.RequestException as e:
                        session.delete()
                        return JsonResponse(send_response("Network error processing payment. Please try again.", False))
                else:
                    session.delete()
                    return JsonResponse(send_response("Invalid session state.", False))
        else:
            return JsonResponse(send_response("Unknown or invalid account", False))

    return JsonResponse({"error": "Invalid request method"}, status=405)



def update_nominee_votes(nominee_code, votes):
    try:
        nominee = Nominees.objects.get(code__iexact=nominee_code)
        nominee.total_vote += votes
        nominee.save()
        return nominee
    except Nominees.DoesNotExist:
        return False
    
# def update_tickets(event_code, tickets):
#     try:
#         ticket_type = TicketType.objects.get(event__code=event_code)
#         ticket_type.available_tickets -= tickets
#         ticket_type.save()
#         return ticket_type
#     except TicketType.DoesNotExist:
#         return False

@csrf_exempt
def webhook_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            print(f'Raw callback data: {data}')
 
            timestamp_str = data.get('Timestamp')
            status = data.get('Status')  # Expecting 'success' or 'failed'
            invoice_no = data.get('InvoiceNo')
            amount = data.get('amount')
            order_id = data.get('Order_id')
            
            
            session = CustomSession.objects.filter(order_id=order_id).first()
            
            
            if not session:
                return JsonResponse({'status': 'error', 'message': 'Session not found'}, status=400)
            
            # Check if session is expired
            if session.is_expired:
                session.delete()
                return JsonResponse({'status': 'error', 'message': 'Session expired'}, status=400)

            if status == 'PAID':
                if session.payment_type == 'VOTE':
                
                    nominee_code = session.candidate_id
                    votes = session.votes
                    
                    nominee = update_nominee_votes(nominee_code, votes)
                    if nominee:
                        PaymentTransaction.objects.create(
                            order_id=order_id,
                            invoice_no=invoice_no,
                            transaction_id=invoice_no,
                            amount=amount,
                            status=status,
                            payment_type='VOTE',
                            nominee_code=nominee_code,
                            votes=votes,
                            category=nominee.category,
                            timestamp=timestamp_str
                        )
                        send_sms_to_voter(phone_number=session.msisdn, nominee_code=nominee_code, category=nominee.category, amount=amount, transaction_id=invoice_no)
                        send_sms_to_nominee_for_vote(phone_number=nominee.phone_number, nominee_code=nominee_code, vote=votes, phone=session.msisdn, transaction_id=invoice_no)
                        session.delete()
                        return JsonResponse({'status': 'success', 'message': 'Votes updated successfully'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Nominee not found'})
                 # Handle Ticketing
                elif session.payment_type == 'TICKET':
                    # ticket_type = update_tickets(event_code, tickets)
                    try:
                        ticket_type = TicketType.objects.get(id=session.ticket_type_id, event__code=session.event_id)
                        ticket_type.available_tickets -= session.tickets
                        ticket_type.save()
                        
                        event_code = session.event_id
                        tickets = session.tickets
                        ticket_name = ticket_type.name
                        event_category = ticket_type.event.name
                        
                        PaymentTransaction.objects.create(
                            order_id=order_id,
                            invoice_no=invoice_no,
                            transaction_id=invoice_no,
                            amount=amount,
                            status=status,
                            payment_type='TICKET',
                            event_code=event_code,
                            tickets=tickets,
                            ticket_type=ticket_name,
                            event_category=event_category,
                            timestamp=timestamp_str
                        )
                        # Send SMS with ticket details
                        # send_ticket_sms(
                        #     phone_number=session.msisdn,  
                        #     event_name=ticket_type.event.name,
                        #     ticket_count=session.tickets,
                        #     amount=amount,
                        #     event_date=ticket_type.event.end_date,
                        #     reference=order_id
                        # )
                        session.delete()
                        return JsonResponse({'status': 'success', 'message': 'Ticket purchase successful'})
                    
                    except TicketType.DoesNotExist:
                        return JsonResponse({'status': 'error', 'message': 'Invalid Ticket type for event not found'})
                
            else:
                return JsonResponse({'status': 'error', 'message': 'Payment failed'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
        
        except Exception as e:
            print(f'Error: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)