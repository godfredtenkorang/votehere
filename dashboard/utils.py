from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, content_dict={}):
    template = get_template(template_src)
    html = template.render(content_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


import requests
from django.conf import settings

def send_sms_to_new_nominee(name, phone_number, category):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": phone_number,
        "message": f"Congrat {name}, your {category} of the year nomination has been received and under review. We will notify you on the status soon. Voteafric!",
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



def send_mnotify_sms(phone_numbers, message):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    
    # Format phone numbers (ensure they start with country code without +)
    
    
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": phone_numbers,
        "message": message,
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


def send_access_code_to_new_nominee(name, phone_number, access_code, category):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": phone_number,
        "message": f"Dear {name}, \nYou can now check your individual results. Please use this code to access your results: {access_code} for the category {category}. If you have any questions, feel free to contact us. \nThank you. \n\nVoteAfric!",
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
    
    

def request_for_payment_sms(name, phone, amount):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": phone,
        "message": f"Dear {name}, \nYou have successfully requested for GH¢{amount}. You will here from us soon.\nThank you. \n\nVoteAfric!",
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
    
    
def receive_request_for_payment_sms(name, phone, amount, category):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'VOTEAFRIC',
        "recipient[]": '0553912334',  # Replace with the actual phone number to receive the request
        "message": f"New Payment Request\n\nName: {name}, \nPhone: {phone}, \nAmount: GH¢{amount}, \nCategory: {category}",
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