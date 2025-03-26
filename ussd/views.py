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
from datetime import datetime
from django.utils import timezone



from django.views import View

@csrf_exempt
def heroku_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(f'Received webhook data: {data}')

            # Process the webhook data
            event_type = data.get('event')  # Example: 'app.update', 'app.create', etc.

            # Handle different event types
            if event_type == 'app.update':
                # Handle app update
                print("App has been updated.")
            elif event_type == 'app.create':
                # Handle app creation
                print("A new app has been created.")
            # Add additional event handling as needed

            return JsonResponse({'status': 'success'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
        except Exception as e:
            print(f'Error: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
# Helper function to generate random key
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
            
            if msgtype:  # Initial request
                session.level = 'start'
                session.save()
                message = "Welcome to VoteAfric.\nContact: 0553912334\nor: 0558156844\nEnter Nominee's code"
                return JsonResponse(send_response(message, True))
            else:  # Follow-up request
                level = session.level
                if level == 'start':
                    try:
                        nominee = Nominees.objects.get(code__iexact=user_data)
                        message = (
                            f"Confirm Candidate\n"
                            f"Name: {nominee.name}\n"
                            f"Category: {nominee.category}\n"
                            f"1) Confirm\n 2) Cancel"
                        )
                        session.candidate_id = nominee.code
                        session.level = 'candidate'
                        session.save()
                        return JsonResponse(send_response(message, True))
                    
                    except Nominees.DoesNotExist:
                        return JsonResponse(send_response("Invalid nominee code. Please try again.", False))

                elif level == 'candidate':
                    if user_data == '1':
                        session.level = 'votes'
                        session.save()
                        message = "Enter the number of votes. \n\n A vote is 0.50ps."
                        return JsonResponse(send_response(message, True))
                    elif user_data == '2':
                        session.delete()
                        return JsonResponse(send_response("You have cancelled the process.", False))
                    else:
                        return JsonResponse(send_response("Invalid input. Please try again.", False))

                elif level == 'votes':
                    try:
                        votes = int(user_data)
                    except ValueError:
                        return JsonResponse(send_response("Invalid number of votes entered. Please try again.", False))
                    
                    session.level = 'payment'
                    session.votes = votes
                    session.amount = Decimal(votes) * Decimal(0.50)
                    session.save()
                    message = f"You have entered {votes} votes \nTotal amount is GH¢{float(session.amount):.2f}.\n\nPress 1 to proceed."
                    return JsonResponse(send_response(message, True))

                elif level == 'payment':
                    amount = session.amount
                    session.save()
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
                    order_id = str(uuid.uuid4())
                    
                    session_key = session.session_key
                    user_id = session.user_id
                    
                   
                    # secrete = f"{secrete[:4]} {secrete[4:]}"

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
                        'user_id': user_id,
                        'session_key': session_key
                    }

                    headers = {
                        "Content-Type": "application/json",
                    }

                    # Sending payment request
                    response = requests.post(endpoint, json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        session.save()
                        message = f"You are about to pay GH¢{amount:.2f}. Please approve the prompt to make payment."
                        # print(secrete_full)
                        print(hashed_password)
                        print(concat_keys)
                        print(secrete)
                        print(key)
                        return JsonResponse(send_response(message, False))
                    else:
                        return JsonResponse(send_response("Payment request failed. Please try again.", False))

                else:
                    return JsonResponse(send_response("Invalid session state.", False))
        else:
            return JsonResponse(send_response("Unknown or invalid account", False))

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def webhook_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            print(f'Received callback data {data}')
            
            timestamp_str = data.get('Timestamp')
            status = data.get('Status')  # Expecting 'success' or 'failed'
            invoice_no = data.get('InvoiceNo')
            amount = data.get('amount')
            order_id = data.get('Order_id')
            msisdn = data.get('MSISDN')
            
            user_id = data.get('USER_ID')
            # session_key = data.get('session_key')
            
            
            
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            
            transaction = PaymentTransaction(
                order_id=order_id,
                invoice_no=invoice_no,
                amount=amount,
                status=status,
                timestamp=timestamp,
            )
            transaction.save()
            
            # Find related session
            session_key = md5(msisdn.encode('utf-8')).hexdigest()
            session = CustomSession.objects.filter(
                session_key=session_key,
                level='payment'
            ).first()
            
            if not session:
                raise Exception("No active session found for this payment")
            
            if status == 'PAID':
                
                
                
                try:
                    
                    
                    nominee = Nominees.objects.get(code=session.candidate_id)
                    
                    nominee.total_vote += session.votes
                    nominee.save()
                    session.delete()
                except CustomSession.DoesNotExist:
                    print(f'Session with key {session_key} does not exist.')
                except Nominees.DoesNotExist:
                    print(f'Nominee not found.')
            
            return JsonResponse({'status': 'success'}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
        
        except Exception as e:
            print(f'Error: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
