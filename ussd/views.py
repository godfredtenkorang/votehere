from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from payment.models import Nominees
import requests


@csrf_exempt
def ussd(request):
    if request.method == 'POST':
        # session_id = request.POST.get('sessionId')
        # service_code = request.POST.get('serviceCode')
        # phone_number = request.POST.get('phoneNumber')
        # text = request.POST.get('text')
        
        userid = request.POST.get('USERID')
        msisdn = request.POST.get('MSISDN')
        userdata = request.POST.get('USERDATA')
        msgtype = request.POST.get('MSDTYPE')
        sessionid = request.POST.get('SESSIONID')
        network = request.POST.get('NETWORK')
        
        if userid != 'GODEY100':
            def sendResponse(msg, status=True):
                return {
                    'USERID': userid,
                    'MSISDN': msisdn,
                    'MSG': msg,
                    'MSGTYPE': status
                }
                
            
            
            response = {}
            
            session = requests.Session()
            if msgtype == True:
                session.next = 'initialise'
                message = "Welcome to voteafric \n Enter nominee's code"
                response = sendResponse(message, True)
                
            else:
                level = session.next
                if level == 'initialise':
                    message = "Enter number of votes"
                    response = sendResponse(message, True)
                    session.next = 'vote'
                elif level == 'vote':
                    message = "You are voting for Godfred as Most Talented"
                    response = sendResponse(message, True)
                    
            return HttpResponse(response)
        
        

        # if text == "":
        #     response = "CON Welcome to VoteAfric \n contact \n 0553912334 for any challenges \n"
        #     response += "1. Enter nominee's code \n"
            # response += "1. Sport \n"
            # response += "2. political \n"
            # response += "3. Local  \n"
            # response += "4. International"


        # elif text == "1":
        #     response = "CON Enter number of votes \n"
        #     response += "1. GODFRED TENKORANG \n"
            # response += "1. Daily @ N100 \n"
            # response += "2. Weekly @ N50 \n"
            # response += "3. Monthly @ N25 \n"
            # response += "per vote is ¢1.00 \n"

        # elif text == "1*1":
        #     response = "CON You will be charged N100 for your Daily Sports news subscription \n"
        #     response += "1. Auto-Renew \n"
        #     response += "2. One-off Purchase \n"
       
            
        # elif text == "1*1*1":
        #     response = "END thank you for subscribing to our daily sport news plan \n"
        # elif text == "1*1*2":
        #     response = "END thank you for your one-off daily sport news plan \n"

        # elif text == "1*2":
        #     response = "CON You will be charged N50 for our weekly Sports news plan \n"
        #     response += "1. Auto-Renew \n"
        #     response += "2. One-off Purchase \n"
        

        # elif text == "1*2*1":
        #     response = "END thank you for subscribing to our weekly sport news plan \n"
        # elif text == "1*2*2":
        #     response = "END thank you for your one-off weekly sport news plan \n"

        # elif text == "1*3":
        #     response = "CON You will be charged N25 for our monthly Sports news plan \n"
        #     response += "1. Auto-Renew \n"
        #     response += "2. One-off Purchase \n"

        # elif text == "1*3*1":
        #     response = "END thank you for subscribing to our monthly sport news plan \n"
        
        # elif text == "1*3*2":
        #     response = "END thank you for your one-off monthly sport news plan \n"

        # return HttpResponse(response)