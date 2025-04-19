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

def send_ticket_sms(phone_number, event_name, ticket_count, amount, event_date, reference):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    # Format event date
    formatted_date = event_date.strftime('%b %d, %Y at %I:%M %p')
    payload = {
        "key": apiKey,
        "sender": 'voteafric',
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
