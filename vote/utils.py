import requests
from  django.conf import settings


def receive_sms_from_event_organizer(event_name):
    """
    Send OTP to the given phone number.
    Replace the below code with your SMS provider's API integration.
    """
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": '0553912334',
        "message": f"Hello, you have a new event organizer. \n\nEvent Name: {event_name}",
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None