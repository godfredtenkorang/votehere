from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import requests
from django.conf import settings

def render_to_pdf(template_src, content_dict={}):
    template = get_template(template_src)
    html = template.render(content_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def send_sms_ticket(phone_number, name, category, amount, transaction_id):
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
        "message": f"Hello, you have successfully voted for {name} in {category}. GHS{amount} was charged. Trans ID: {transaction_id}",
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