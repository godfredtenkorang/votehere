from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import requests

# Simulate a database of nominees

nominees = {
    'GT1': {'name': 'Godfred Tenkorang', 'category': 'Most Talented'},
    'OA2': {'name': 'Ohene Asare', 'category': 'Best Performer'},
    'SA3': {'name': 'Seth Ansah', 'category': 'Outstanding Leadership'},
}

@csrf_exempt
@require_POST
def ussd(request):
    data = json.loads(request.body)

    def send_response(TheMsg, MsgType=True):
        return {
            'USERID': data['USERID'],
            'MSISDN': data['MSISDN'],
            'MSG': f"{TheMsg}",
            'MSGTYPE': MsgType
        }

    # Simulate valid USERIDs for the sake of this example
    # valid_user_id = ['GODEY100']

    session = request.session
    if data['USERID'] == 'GODEY100':
        if data['MSGTYPE']:
            session['level'] = 'start'
            message = "Welcome to VoteAfric.\n Contact: 0553912334\n or: 0558156844\n Enter Nominee's code"
            response = send_response(message, True)
        else:
            if 'level' in session:
                level = session['level']
                userdata = data['USERDATA']
                if level == 'start':
                    # Simulate fetching user from database with this ID
                    nominee_id = userdata
                    if nominee_id in nominees:
                        nominee = nominees[nominee_id]
                        name = nominee['name']
                        category = nominee['category']
                        message = f"Confirm candidate\nName: {name}\nCategory: {category}1) Confirm\n2) Cancel"
                        session['candidate_id'] = nominee_id
                        session['level'] = 'candidate'
                        response = send_response(message)
                    else:
                        message = 'Invalid nominee code. Please try again.'
                        response = send_response(message, False)
                elif level == 'candidate':
                    if userdata == '1':
                        session['level'] = 'votes'
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
                    message = f"You have entered {votes} votes"
                    response = send_response(message, True)
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


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def ussd(request):
#     if request.method == 'POST':
        
#         userid = request.POST.get('USERID')
#         msisdn = request.POST.get('MSISDN')
#         userdata = request.POST.get('USERDATA')
#         msgtype = request.POST.get('MSDTYPE')
#         sessionid = request.POST.get('SESSIONID')
#         network = request.POST.get('NETWORK')
        
#         def send_response(TheMsg, MsgType=True):
#             return {
#                 'USERID': userid,
#                 'MSISDN': msisdn,
#                 'MSG': f"{TheMsg}",
#                 'MSGTYPE': MsgType
#             }
            
        
#         if userid == 'GODEY100':
#             if msgtype:
#                 session = request.session
#                 session['level'] = 'start'
#                 message = "Welcome to vote afric \n Enter nominee's code"
#                 response_data = send_response(message, True) 
#             else:
#                 if 'level' in session:
#                     level = session['level']
#                     userdata = userdata
#                     if level == 'start':
                        
                        
#                         name = 'Godfred Yaw Tenkorang'
#                         message = f"Confirm candidate\nName: {name}\n1) Confirm\n2) Cancel"
#                         session['candidate_id'] = userdata
#                         session['level'] = 'candidate'
                        
#                         response_data = send_response(message) 
#                     elif level == 'candidate':
#                         if userdata == 1:
#                             session['level'] = 'votes'
#                             # session['votes'] = userdata
#                             message = "Enter the number of votes"
#                             response_data = send_response(message, True) 
#                         elif userdata == 2:
                            
#                             message = "You have cancelled"
#                             response_data = send_response(message, False) 
#                             session.clear()
#                         else:
#                             session.clear()
#                             message = "You have entered an invalid data"
#                             response_data = send_response(message, False) 
#                     elif level == 'votes':
#                         votes = userdata
#                         message = f"You have entered {votes} votes"
#                         response_data = send_response(message, True) 
#                     else:
#                         message = "Welcome to VoteAfric"
#                         response_data = send_response(message, False) 
#                 else:
#                     message = "You are not in a session"
#                     response_data = send_response(message, False) 
#         else:
#             message = "you have entered a wrong value"
#             response_data = send_response(message, False) 
                        
#         return JsonResponse(response_data)

# def ussd(request):
#     if request.method == 'POST':
        
#         userid = request.POST.get('USERID')
#         msisdn = request.POST.get('MSISDN')
#         userdata = request.POST.get('USERDATA')
#         msgtype = request.POST.get('MSDTYPE')
#         sessionid = request.POST.get('SESSIONID')
#         network = request.POST.get('NETWORK')
        
#         def sendResponse(msg, status=True):
#             return {
#                 'USERID': userid,
#                 'MSISDN': msisdn,
#                 'MSG': msg,
#                 'MSGTYPE': status
#             }
            
        
#         if userid == 'GODEY100':
        
#             response_data = {}
            
#             session = requests.Session()
#             if msgtype == True:
#                 session.next = 'initialise'
#                 message = "Welcome to voteafric \n Enter nominee's code"
#                 response_data = sendResponse(message, True)
                
#             else:
#                 level = session.next
#                 if level == 'initialise':
#                     message = "Enter number of votes"
#                     response_data = sendResponse(message, True)
#                     session.next = 'vote'
#                 elif level == 'vote':
#                     message = "You are voting for Godfred as Most Talented"
#                     response_data = sendResponse(message, True)
#                     session.next = 'vote'
                    
#                 return HttpResponse(response_data)


# def ussd(request): 
    # if request.method == 'POST':
        # Extracting data from the POST request
        # userid = request.POST.get('USERID')
        # msisdn = request.POST.get('MSISDN')
        # userdata = request.POST.get('USERDATA')
        # msgtype = request.POST.get('MSGTYPE')
        # sessionid = request.POST.get('SESSIONID')
        # network = request.POST.get('NETWORK')

        # def send_response(msg, msgtype='response'):
            # Prepare the response data in the required format
            # return {
            #     'USERID': userid,
            #     'MSISDN': msisdn,
            #     'MSG': msg,
            #     'MSGTYPE': msgtype
            # }

        # Check if the user is authorized (e.g., using userid)
        # if userid == 'GODEY100':
        #     if msgtype == 'INITIALIZE':
                # If it's an initialization message, send the welcome message
                # message = "Welcome to VoteAfrica. Enter nominee's code."
                # return JsonResponse(send_response(message))

            # elif msgtype == 'RESPONSE':
                # Process the user's response based on the session
                # session = request.session
                # level = session.get('level')

                # if level == 'initial':
                    # Assuming the first input is the nominee's code
                    # nominee_code = userdata.strip()
                    # Check if the nominee code exists in your database (Nominees model)
                    # try:
                    #     nominee = Nominees.objects.get(code=nominee_code)
                    #     message = f"You are voting for {nominee.name}. Enter number of votes."
                        # session['nominee'] = nominee  # Store nominee in session for future use
                        # session['level'] = 'vote'
                #     except Nominees.DoesNotExist:
                #         message = "Invalid nominee code. Please enter a valid code."
                #         session['level'] = 'initial'

                #     return JsonResponse(send_response(message))

                # elif level == 'vote':
                    # Assuming the second input is the number of votes
                    # try:
                    #     num_votes = int(userdata.strip())
                        # Perform further processing (e.g., record votes in your database)
    #                     nominee = session.get('nominee')
    #                     message = f"You have successfully voted {num_votes} votes for {nominee.name}. Thank you!"
    #                     session['level'] = 'initial'  # Reset session for the next interaction
    #                 except ValueError:
    #                     message = "Invalid input. Please enter a number for the votes."
    #                     session['level'] = 'vote'

    #                 return JsonResponse(send_response(message))

    #     else:
    #         message = "You are not authorized to access this service."
    #         return JsonResponse(send_response(message, 'error'))

    # else:
    #     return JsonResponse({'error': 'Method not allowed.'}, status=405)