import requests
from django.conf import settings

def send_donation_sms(phone_number, cause_name, amount, reference):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    # Format event date
    
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": phone_number,
        "message": 
            f"Thank you for your donation to {cause_name}!\n"
            f"Amount: GH¢{float(amount):.2f}\n"
            f"Reference: {reference}\n\n"
            "Your support makes a difference.\n"
            "VoteAfric - Building a better future together",
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
