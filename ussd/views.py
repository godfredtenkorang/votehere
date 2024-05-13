from django.http import JsonResponse
from payment.models import Nominees
import requests

def ussd(request):
    if request.method == 'POST':
        
        userid = request.POST.get('USERID')
        msisdn = request.POST.get('MSISDN')
        userdata = request.POST.get('USERDATA')
        msgtype = request.POST.get('MSDTYPE')
        sessionid = request.POST.get('SESSIONID')
        network = request.POST.get('NETWORK')
        
        def sendResponse(msg, status=True):
            return {
                'USERID': userid,
                'MSISDN': msisdn,
                'MSG': msg,
                'MSGTYPE': status
            }
            
        
        if userid == 'GODEY100':
        
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
                    
                return JsonResponse(response)
