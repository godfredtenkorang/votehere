from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomSession, PaymentTransaction
import json
import hashlib
import uuid
import requests
from decimal import Decimal
import random
from django.conf import settings

# Sample nominees data
nominees = {
    'GT1': {'name': 'Godfred Tenkorang', 'category': 'Most Talented'},
    'OA2': {'name': 'Ohene Asare', 'category': 'Best Performer'},
    'SA3': {'name': 'Seth Ansah', 'category': 'Outstanding Leadership'},
}

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
        user_data = data.get('USERDATA')
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
            session_key = hashlib.md5(msisdn.encode('utf-8')).hexdigest()
            session, created = CustomSession.objects.get_or_create(session_key=session_key, defaults={'user_id': user_id})
            
            if msgtype:  # Initial request
                session.level = 'start'
                session.save()
                message = "Welcome to VoteAfric.\nContact: 0553912334\nor: 0558156844\nEnter Nominee's code"
                return JsonResponse(send_response(message, True))
            else:  # Follow-up request
                level = session.level
                if level == 'start':
                    nominee_id = user_data
                    if nominee_id in nominees:
                        nominee = nominees[nominee_id]
                        name = nominee['name']
                        category = nominee['category']
                        message = f"Confirm candidate\nName: {name}\nCategory: {category}\n1) Confirm\n2) Cancel"
                        session.candidate_id = nominee_id
                        session.level = 'candidate'
                        session.save()
                        return JsonResponse(send_response(message, True))
                    else:
                        return JsonResponse(send_response("Invalid nominee code. Please try again.", False))

                elif level == 'candidate':
                    if user_data == '1':
                        session.level = 'votes'
                        session.save()
                        message = "Enter the number of votes. \n\n A vote is GH¢1.00."
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
                    session.amount = Decimal(votes) * Decimal(1.00)
                    session.save()
                    message = f"You have entered {votes} votes \nTotal amount is GH¢{float(session.amount):.2f}.\n\nPress 1 to proceed."
                    return JsonResponse(send_response(message, True))

                elif level == 'payment':
                    amount = session.amount * 1
                    telephone = msisdn
                    network_type = network
                    endpoint = "https://api.paystack.co/charge"
                    public_key = f"{settings.PAYSTACK_PUBLIC_KEY}"
                    secret_key = f"{settings.PAYSTACK_SECRET_KEY}"
                    email = f"{msisdn}@voteafric.com"
                    # Create a unique transaction reference
                    reference = str(uuid.uuid4())
                    
                    amount_in_kobo = int(Decimal(amount))  # Convert to kobo
                    print(amount_in_kobo)
                    
                    payload = {
                        'email': email,
                        'amount': 1,
                        'currency': 'GHS',  # Set appropriate currency
                        "ussd": {
                            "type": "ussd",
                            "bank": "057",
                        },
                         "metadata": {
                            "phone": msisdn,
                            "network": network_type,
                            "votes": session.votes
                        },
                        "reference": reference,
                        
                    }
                    
                    
                    headers = {
                        "Authorization": f"Bearer {secret_key}",  # Replace with your actual secret key
                        "Content-Type": "application/json",
                    }
                    
                     # Sending payment request to Paystack
                    response = requests.post(endpoint, json=payload, headers=headers)

                    if response.status_code == 200:
                        message = f"You are about to pay GH¢{amount:.2f}. Please follow the USSD code prompt sent to your phone to complete the payment."
                        return JsonResponse(send_response(message, False))

                    else:
                        error_data = response.json()
                        print(error_data)
                        return JsonResponse(send_response(f"Payment request failed: {error_data.get('message', 'Please try again.')}", False))
                # elif level == 'payment':
                #     amount = session.amount
                #     endpoint = "https://api.nalosolutions.com/payplus/api/"
                #     telephone = msisdn
                #     network_type = network
                #     username = 'votfric_gen'
                #     password = 'bVdwy86yoWtdZcW'
                #     merchant_id = 'NPS_000288'
                #     key = str(2345)
                #     hashed_password = hashlib.md5(password.encode()).hexdigest()
                #     concat_keys = username + key + hashed_password
                #     secrete = hashlib.md5(concat_keys.encode()).hexdigest()
                #     callback = 'https://voteafric.com/ussd/callback/'
                #     item_desc = 'Payment for vote'
                #     order_id = str(uuid.uuid4())

                #     # Payment payload
                #     payload = {
                #         'payby': network_type,
                #         'order_id': order_id,
                #         'customerNumber': telephone,
                #         'customerName': telephone,
                #         'isussd': 1,
                #         'amount': str(amount),
                #         'merchant_id': merchant_id,
                #         'secrete': str(secrete),
                #         'key': key,
                #         'callback': callback,
                #         'item_desc': item_desc
                #     }

                #     headers = {
                #         "Content-Type": "application/json",
                #         "Accept": "application/json"
                #     }

                #     # Sending payment request
                #     response = requests.post(endpoint, json=payload, headers=headers)
                    
                #     if response.status_code == 200:
                #         session.delete()
                #         message = f"You are about to pay GH¢{amount:.2f}. Please approve the prompt to make payment."
                #         return JsonResponse(send_response(message, False))
                #     else:
                #         return JsonResponse(send_response("Payment request failed. Please try again.", False))

                else:
                    return JsonResponse(send_response("Invalid session state.", False))
        else:
            return JsonResponse(send_response("Unknown or invalid account", False))

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Extract data from the callback
            transaction_id = data.get('transaction_id')
            status = data.get('status')
            amount = data.get('amount')
            customer_number = data.get('customerNumber')

            # Update the PaymentTransaction record
            PaymentTransaction.objects.filter(transaction_id=transaction_id).update(
                status=status,
                amount=amount
            )

            # Handle session based on payment status
            session = CustomSession.objects.filter(user_id=customer_number).first()

            if session:
                if status == "success":
                    # Payment succeeded, delete session
                    session.delete()
                    return JsonResponse({'status': 'success', 'message': 'Payment processed and session deleted.'}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Payment failed, session retained.'}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': 'Session not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



import json
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PaymentTransaction

@csrf_exempt
def paystack_webhook(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload from Paystack
            payload = json.loads(request.body.decode('utf-8'))
            event = payload.get('event')  # The event type (e.g., charge.success)
            data = payload.get('data')  # Payment data
            
            if event == 'charge.success':
                transaction_id = data.get('reference')  # Paystack reference
                amount_paid = data.get('amount') / 100  # Convert to original currency (in cedis)
                customer_email = data.get('customer', {}).get('email', None)
                status = data.get('status')  # Should be 'success'

                # Update your PaymentTransaction model
                PaymentTransaction.objects.filter(transaction_id=transaction_id).update(
                    status=status,
                    amount=amount_paid
                )
                
                # You could perform additional actions like sending notifications

                return JsonResponse({'status': 'success'}, status=200)
            else:
                # Handle other Paystack events like 'charge.failed', etc.
                return JsonResponse({'status': 'ignored', 'message': 'Unhandled event'}, status=400)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
