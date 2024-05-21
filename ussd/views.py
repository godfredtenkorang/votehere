from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import hashlib
import uuid
import requests



nominees = {
    'GT1': {'name': 'Godfred Tenkorang', 'category': 'Most Talented'},
    'OA2': {'name': 'Ohene Asare', 'category': 'Best Performer'},
    'SA3': {'name': 'Seth Ansah', 'category': 'Outstanding Leadership'},
}

@csrf_exempt
@require_POST
def ussd_api(request):
    data = json.loads(request.body.decode('utf-8'))

    def send_response(TheMsg, MsgType=True):
        return {
            'USERID': data['USERID'],
            'MSISDN': data['MSISDN'],
            'MSG': f"{TheMsg}",
            'MSGTYPE': MsgType
        }

    # valid_user_id = ['GODEY100']

    session = request.session
    if data['USERID'] == 'GODEY100':
        if data['MSGTYPE']:
            session['level'] = 'start'
            session.save()
            message = "Welcome to VoteAfric.\n Contact: 0553912334\n or: 0558156844\n Enter Nominee's code"
            response = send_response(message, True)
        else:
            if session.get('level'):
                level = session['level']
                userdata = data['USERDATA']
                if level == 'start':
                    nominee_id = userdata
                    if nominee_id in nominees:
                        nominee = nominees[nominee_id]
                        name = nominee['name']
                        category = nominee['category']
                        message = f"Confirm candidate\nName: {name}\nCategory: {category}1) Confirm\n2) Cancel"
                        session['candidate_id'] = nominee_id
                        session['level'] = 'candidate'
                        session.save()
                        response = send_response(message, False)
                    else:
                        message = 'Invalid nominee code. Please try again.'
                        response = send_response(message, False)
                elif level == 'candidate':
                    if userdata == '1':
                        session['level'] = 'votes'
                        session.save()
                        message = "Enter the number of votes"
                        response = send_response(message, True)
                    elif userdata == '2':
                        message = "You have cancelled"
                        response = send_response(message, False)
                        session.flush()
                    else:
                        session.flush()
                        message = "You have entered invalid data"
                        response = send_response(message, False)
                elif level == 'votes':
                    votes = userdata
                    session['level'] = 'payment'
                    session.save()
                    message = f"You have entered {votes} votes"
                    response = send_response(message, True)
                elif level == 'payment':
                    amount = userdata
                    endpoint = "https://api.nalosolutions.com/payplus/api/"
                    telephone = data['MSISDN']
                    network = data['NETWORK']
                    username = 'votfric_gen'
                    password = 'bVdwy86yoWtdZcW'
                    merchant_id = 'NPS_000288'
                    key = 'Nrkl)CYr'
                    hashed_password = hashlib.md5(password.encode()).hexdigest()
                    concat_keys = username + key + hashed_password
                    secrete = hashlib.md5(concat_keys.encode()).hexdigest()
                    callback = 'https://voteafric.com/ussd/ussd/'
                    item_desc = f'Payment for vote'
                    order_id = uuid.uuid4()

                    payload = dict(payby=network, order_id=order_id, customerNumber=telephone,
                                   customerName=telephone, isussd=1, amount=amount, merchant_id=merchant_id,
                                   secrete=secrete, key=key, callback=callback, item_desc=item_desc)
                    headers = {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    }

                    message = f"You are about to pay {amount}"
                    response = send_response(message, False)

                    requests.post(endpoint, headers=headers, data=payload)
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