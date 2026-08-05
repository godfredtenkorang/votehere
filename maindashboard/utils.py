import requests
from django.conf import settings


def send_approved_sms(phone_number, name, category, amount):
    """
    Send SMS notification for ticket purchase.
    Replace the below code with your SMS provider's API integration.
    """
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": phone_number,
        "message": f"""
        Dear {name},
        
        Your payment of GHS{amount} for {category} has approved.
        
        Thank you for your patronage!
        VoteAfric Team
        """,
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