from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomSession, PaymentTransaction
from .utils import send_sms
import json
import hashlib
import uuid
import requests
from decimal import Decimal
import random

nominees = {
    'GT1': {'name': 'Godfred Tenkorang', 'category': 'Most Talented'},
    'OA2': {'name': 'Ohene Asare', 'category': 'Best Performer'},
    'SA3': {'name': 'Seth Ansah', 'category': 'Outstanding Leadership'},
}

def generate_random_key():
    return random.randint(1000, 9999)

@csrf_exempt
def ussd_api(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        user_id = data.get('USERID')
        msisdn = data.get('MSISDN')
        user_data = data.get('USERDATA')
        msgtype = data.get('MSGTYPE')
        network = data.get('NETWORK')

        def send_response(msg, msgtype=True):
            return {
                'USERID': user_id,
                'MSISDN': msisdn,
                'MSG': msg,
                'MSGTYPE': msgtype
            }

        if user_id == 'GODEY100':
            session_key = hashlib.md5(msisdn.encode('utf-8')).hexdigest()
            
            session, created = CustomSession.objects.get_or_create(session_key=session_key, defaults={'user_id':user_id})
            if msgtype:
                session.level = 'start'
                session.save()
                message = "Welcome to VoteAfric.\nContact: 0553912334\nor: 0558156844\nEnter Nominee's code"
                response = send_response(message, True)
            else:
                level = session.level
                if level:
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
                            response = send_response(message)
                        else:
                            message = 'Invalid nominee code. Please try again.'
                            response = send_response(message, False)
                    elif level == 'candidate':
                        if user_data == '1':
                            session.level = 'votes'
                            session.save()
                            message = "Enter the number of votes"
                            response = send_response(message, True)
                        elif user_data == '2':
                            message = "You have cancelled"
                            response = send_response(message, False)
                            session.delete()
                        else:
                            session.delete()
                            message = "You have entered invalid data"
                            response = send_response(message, False)
                    elif level == 'votes':
                        votes = int(user_data)
                        session.level = 'payment'
                        session.votes = votes
                        session.amount = Decimal(votes) * Decimal(1.00)
                        session.save()
                        message = f"You have entered {votes} votes \nTotal amount is GH¢{float(session.amount):.2f}.\n\nA vote is GH¢1.00. Press 1 to proceed."
                        response = send_response(message, True)
                    elif level == 'payment':
                        amount = float(session.amount)
                        session.save()
                        endpoint = "https://api.nalosolutions.com/payplus/api/"
                        telephone = msisdn
                        network = network
                        username = 'votfric_gen'
                        password = 'bVdwy86yoWtdZcW'
                        merchant_id = 'NPS_000288'
                        key = str(generate_random_key())
                        hashed_password = hashlib.md5(password.encode()).hexdigest()
                        concat_keys = username + key + hashed_password
                        secrete = hashlib.md5(concat_keys.encode()).hexdigest()
                        callback = 'https://voteafric.com/callback/'
                        item_desc = 'Payment for vote'
                        order_id = str(uuid.uuid4())
                        

                        payload = {
                            'payby': network,
                            'order_id': order_id,
                            'customerNumber': telephone,
                            'customerName': telephone,
                            'isussd': 1,
                            'amount': str(amount),
                            'merchant_id': merchant_id,
                            'secrete': secrete,
                            'key': key,
                            'callback': callback,
                            'item_desc': item_desc
                        }
                        headers = {
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                        }
                        
                        
                        # message = f"You are about to pay GH¢{amount}"
                        # response = send_response(message, False)
                        # requests.post(endpoint, headers=headers, json=payload)
                        
                        # send_sms(phone_number=telephone, message="Thank you for voting. Dial *920*106# to vote for your favourite nominee.")
                        # session.delete()
                        
                        logger.info(f"Sending payment request: {payload}")
                        
                        

                        try:
                            response = requests.request("POST", endpoint, headers=headers, data=payload)
                            logger.info(f"Received response: {response.status_code} - {response.text}")
                            if response.status_code == 200:
                                message = f"You are about to pay GH¢{amount}"
                                send_sms(phone_number=telephone, message="Thank you for voting. Dial *920*106# to vote for your favourite nominee.")
                            else:
                                message = "Payment request failed. Please try again."
                        except Exception as e:
                            logger.error(f"Error sending payment request: {e}")
                            message = "An error occurred while processing your payment. Please try again."

                        
                        response = send_response(message, False)
                        if session.session_key is not None:
                            session.delete()
                        
                    else:
                        message = "WKHKYD"
                        response = send_response(message, False)
                else:
                    message = "You are not in a session"
                    response = send_response(message, False)
        else:
            message = "Unknown or invalid account"
            response = send_response(message, False)

        return JsonResponse(response, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)




import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Extract data from the callback
            transaction_id = data.get('transaction_id')
            status = data.get('status')
            amount = data.get('amount')
            
            logger.info(f"Received payment callback: {data}")

            # Update the database
            PaymentTransaction.objects.filter(transaction_id=transaction_id).update(
                status=status,
                amount=Decimal(amount)
            )

            # Respond to the external service
            return JsonResponse({'status': 'success'}, status=200)

        except Exception as e:
            print(f"Error processing callback: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)