from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ussd(request):
    if request.method == 'POST':
        
        userid = request.POST.get('USERID')
        msisdn = request.POST.get('MSISDN')
        userdata = request.POST.get('USERDATA')
        msgtype = request.POST.get('MSDTYPE')
        sessionid = request.POST.get('SESSIONID')
        network = request.POST.get('NETWORK')
        
        def send_response(TheMsg, MsgType=True):
            return {
                'USERID': userid,
                'MSISDN': msisdn, 
                'MSG': TheMsg,
                'MSGTYPE': MsgType,
            }
        
        if userid == 'GODEY100':
            session = request.session

            if msgtype == '1':  # Assuming msgtype for initialization is '1'
                session['level'] = 'start'
                message = "Welcome to VoteAfric \n Enter nominee's code"
                response_data = send_response(message, msgtype=True)
            else:
                level = session.get('level')
                
                if level == 'start':
                    session['level'] = 'candidate'
                    session['candidate_id'] = userdata
                    name = 'Godfred Yaw Tenkorang'  # This should be fetched from your database
                    message = f"Confirm candidate\nName: {name}\n1) Confirm\n2) Cancel"
                    response_data = send_response(message, msgtype=True)
                
                elif level == 'candidate':
                    if userdata == '1':  # Assuming '1' is the confirmation input
                        session['level'] = 'votes'
                        message = "Enter the number of votes"
                        response_data = send_response(message, msgtype=True)
                    elif userdata == '2':  # Assuming '2' is the cancellation input
                        session.flush()
                        message = "You have cancelled"
                        response_data = send_response(message, msgtype=False)
                    else:
                        session.flush()
                        message = "You have entered invalid data"
                        response_data = send_response(message, msgtype=False)
                
                elif level == 'votes':
                    try:
                        votes = int(userdata)
                        candidate_id = session.get('candidate_id')
                        # Here you would typically save the votes to your database
                        message = f"You have entered {votes} votes"
                        response_data = send_response(message, msgtype=False)
                        session.flush()  # Clear the session after voting
                    except ValueError:
                        message = "Invalid input. Please enter a valid number of votes."
                        response_data = send_response(message, msgtype=True)
                
                else:
                    message = "Welcome to VoteAfric"
                    response_data = send_response(message, msgtype=False)
        
        else:
            message = "You have entered a wrong value"
            response_data = send_response(message)
                        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

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