from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib
import uuid
import requests

# Nominee details
nominees = {
    'GT1': {'name': 'Godfred Tenkorang', 'category': 'Most Talented'},
    'OA2': {'name': 'Ohene Asare', 'category': 'Best Performer'},
    'SA3': {'name': 'Seth Ansah', 'category': 'Outstanding Leadership'},
}

def generate_session_id(msisdn):
    msisdn_bytes = msisdn.encode('utf-8')
    hash_object = hashlib.md5(msisdn_bytes)
    session_id = hash_object.hexdigest()
    return session_id

@csrf_exempt
def ussd_api(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        user_id = data.get('USERID')
        msisdn = data.get('MSISDN')
        user_data = data.get('USERDATA')
        msgtype = data.get('MSGTYPE')
        network = data.get('NETWORK')
        session_id = generate_session_id(msisdn=msisdn)

        def send_response(msg, msgtype=True):
            return {
                'USERID': user_id,
                'MSISDN': msisdn,
                'MSG': msg,
                'MSGTYPE': msgtype
            }

        if user_id == 'GODEY100':
            session_id = generate_session_id(msisdn)
            request.session['session_id'] = session_id
            if msgtype:
                request.session['level'] = 'start'
                message = "Welcome to VoteAfric.\nContact: 0553912334\nor: 0558156844\nEnter Nominee's code"
                response = send_response(message, True)
            else:
                level = request.session.get('level')
                if level:
                    if level == 'start':
                        nominee_id = user_data
                        if nominee_id in nominees:
                            nominee = nominees[nominee_id]
                            name = nominee['name']
                            category = nominee['category']
                            message = f"Confirm candidate\nName: {name}\nCategory: {category}\n1) Confirm\n2) Cancel"
                            request.session['candidate_id'] = nominee_id
                            request.session['level'] = 'candidate'
                            response = send_response(message)
                        else:
                            message = 'Invalid nominee code. Please try again.'
                            response = send_response(message, False)
                    elif level == 'candidate':
                        if user_data == '1':
                            request.session['level'] = 'votes'
                            message = "Enter the number of votes"
                            response = send_response(message, True)
                        elif user_data == '2':
                            message = "You have cancelled"
                            response = send_response(message, False)
                            request.session.flush()
                        else:
                            request.session.flush()
                            message = "You have entered invalid data"
                            response = send_response(message, False)
                    elif level == 'votes':
                        votes = user_data
                        request.session['level'] = 'payment'
                        message = f"You have entered {votes} votes"
                        response = send_response(message, True)
                    elif level == 'payment':
                        amount = user_data
                        endpoint = "https://api.nalosolutions.com/payplus/api/"
                        telephone = msisdn
                        network = network
                        username = 'votfric_gen'
                        password = 'bVdwy86yoWtdZcW'
                        merchant_id = 'NPS_000288'
                        key = 'Nrkl)CYr'
                        hashed_password = hashlib.md5(password.encode()).hexdigest()
                        concat_keys = username + key + hashed_password
                        secrete = hashlib.md5(concat_keys.encode()).hexdigest()
                        callback = 'https://voteafric.com/ussd/ussd/'
                        item_desc = 'Payment for vote'
                        order_id = str(uuid.uuid4())

                        payload = {
                            'payby': network,
                            'order_id': order_id,
                            'customerNumber': telephone,
                            'customerName': telephone,
                            'isussd': 1,
                            'amount': amount,
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

                        message = f"You are about to pay {amount}"
                        response = send_response(message, False)
                        requests.post(endpoint, headers=headers, json=payload)
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
