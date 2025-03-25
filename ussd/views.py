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



from django.views import View

class AystackWebhookView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({"message": "Webhook received"}, status=200)

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
                    callback = 'https://voteafric.com/ussd/callback/'
                    item_desc = 'Payment for vote'
                    order_id = str(uuid.uuid4())
                    
                   
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
                        'item_desc': item_desc
                    }

                    headers = {
                        "Content-Type": "application/json",
                    }

                    # Sending payment request
                    response = requests.post(endpoint, json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        session.delete()
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
def payment_callback(request):
    if request.method == 'POST':
        try:
            # First, log the raw request body for debugging
            raw_body = request.body.decode('utf-8')
            print(f"Raw callback received: {raw_body}")
            
            try:
                data = json.loads(raw_body)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid JSON format'
                }, status=400)

            # Log the parsed data
            print(f"Parsed callback data: {data}")

            # Validate required fields
            required_fields = ['order_id', 'transaction_id', 'status', 'amount', 'customerNumber']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"Missing required fields: {missing_fields}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing required fields: {", ".join(missing_fields)}'
                }, status=400)

            # Extract data with additional validation
            order_id = data.get('order_id')
            transaction_id = data.get('transaction_id')
            status = data.get('status', '').lower()
            amount = data.get('amount')
            customer_number = data.get('customerNumber')
            network = data.get('network', 'unknown')

            # Additional validation for numeric fields
            try:
                amount = Decimal(amount)
            except (TypeError, ValueError) as e:
                print(f"Invalid amount format: {amount}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid amount format'
                }, status=400)

            # Find or create transaction record
            transaction, created = PaymentTransaction.objects.get_or_create(
                transaction_id=transaction_id,
                defaults={
                    'order_id': order_id,
                    'status': status,
                    'amount': amount,
                    'customer_number': customer_number,
                    'network': network,
                    'raw_response': json.dumps(data)
                }
            )

            if not created:
                transaction.status = status
                transaction.amount = amount
                transaction.save()

            # Find session - note: customer_number might need formatting
            # Ensure MSISDN format matches what you stored in session
            if customer_number.startswith("0"):
                formatted_number = "233" + customer_number[1:]
            elif not customer_number.startswith("233"):
                formatted_number = "233" + customer_number
            else:
                formatted_number = customer_number

            session = CustomSession.objects.filter(
                session_key=md5(formatted_number.encode('utf-8')).hexdigest(),
                level='payment'
            ).first()

            if not session:
                print(f"No active session found for customer: {formatted_number}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'No active voting session found'
                }, status=404)

            # Process successful payment
            if status == "success":
                try:
                    nominee = Nominees.objects.get(code=session.candidate_id)
                    nominee.total_vote += session.votes
                    nominee.save()
                    
                    # Send confirmation (optional)
                    print(f"Successfully added {session.votes} votes to {nominee.name}")
                    
                    session.delete()
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Payment processed and votes counted'
                    }, status=200)
                
                except Nominees.DoesNotExist:
                    print(f"Nominee not found with code: {session.candidate_id}")
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Nominee not found'
                    }, status=404)
                
                except Exception as e:
                    print(f"Error updating nominee: {str(e)}")
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Error processing votes'
                    }, status=500)

            # Handle failed payment
            return JsonResponse({
                'status': 'success',  # Still return success to payment gateway
                'message': 'Callback received (payment failed)'
            }, status=200)

        except Exception as e:
            print(f"Unexpected error in callback: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)