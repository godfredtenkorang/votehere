import requests

def send_sms(phone_number, message):
    # Implement your SMS sending logic here
    # For example, using an external API
    api_url = "https://api.yoursmsprovider.com/send"
    payload = {
        'phone_number': phone_number,
        'message': message,
        'api_key': 'your_api_key'
    }
    response = requests.post(api_url, data=payload)
    return response.status_code == 200