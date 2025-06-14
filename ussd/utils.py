import requests
from django.conf import settings

def send_sms_to_voter(phone_number, nominee_code, category, amount, transaction_id):
    """
    Send OTP to the given phone number.
    Replace the below code with your SMS provider's API integration.
    """
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": phone_number,
        "message": f"Hello, you have successfully voted for {nominee_code} in {category}. GHS{amount} was charged. Trans ID: {transaction_id}",
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
    
    
def send_sms_to_nominee_for_vote(phone_number, nominee_code, vote, phone, transaction_id):
    """
    Send OTP to the given phone number.
    Replace the below code with your SMS provider's API integration.
    """
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": phone_number,
        "message": f"Hello {nominee_code}, you have received {vote} votes from {phone}. Trans ID: {transaction_id}",
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
    
    
def send_donation_sms(phone_number, cause_name, amount, reference):
    
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": phone_number,
        "message": f"Thank you for your donation to {cause_name}!\n" f"Amount: GH¢{float(amount):.2f}\n" f"Reference: {reference}\n\n" "Your support makes a difference.\n" "VoteAfric - Building a better future together",
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
    
def send_ticket_sms(phone_number, event_name, ticket_count, amount, event_date, reference):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    # Format event date
    formatted_date = event_date.strftime('%b %d, %Y at %I:%M %p')
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": phone_number,
        "message": 
            f"Your ticket(s) for {event_name}\n"
            f"Quantity: {ticket_count}\n"
            f"Amount: GH¢{float(amount):.2f}\n"
            f"Event Date: {formatted_date}\n"
            f"Ref: {reference}\n"
            f"Present this code at the venue."
        ,
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
