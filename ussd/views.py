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
from payment.models import Nominees

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
                    try:
                        nominee = Nominees.objects.get(code=user_data)
                        message = (
                            f"Confirm Candidate\n"
                            f"Name: {nominee.name}"
                            f"Category: {nominee.category}"
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
                    amount = session.amount
                    endpoint = "https://api.nalosolutions.com/payplus/api/"
                    telephone = msisdn
                    network_type = network
                    username = 'votfric_gen'
                    password = 'bVdwy86yoWtdZcW'
                    merchant_id = 'NPS_000288'
                    key = str(2345)
                    hashed_password = hashlib.md5(password.encode()).hexdigest()
                    concat_keys = username + key + hashed_password
                    secrete = hashlib.md5(concat_keys.encode()).hexdigest()
                    callback = 'https://voteafric.com/ussd/callback/'
                    item_desc = 'Payment for vote'
                    order_id = str(uuid.uuid4())

                    # Payment payload
                    payload = {
                        'payby': network_type,
                        'order_id': order_id,
                        'customerNumber': telephone,
                        'customerName': telephone,
                        'isussd': 1,
                        'amount': str(amount),
                        'merchant_id': merchant_id,
                        'secrete': str(secrete),
                        'key': key,
                        'callback': callback,
                        'item_desc': item_desc
                    }

                    headers = {
                        "Content-Type": "application/json",
                    }

                    # Sending payment request
                    response = requests.post(endpoint, data=payload, headers=headers)
                    
                    if response.status_code == 200:
                        session.delete()
                        message = f"You are about to pay GH¢{amount:.2f}. Please approve the prompt to make payment."
                        return JsonResponse(send_response(message, False))
                    else:
                        return JsonResponse(send_response("Payment request failed. Please try again.", False))

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

