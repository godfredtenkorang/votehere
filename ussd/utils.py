import requests

def send_sms(phone_number, message):
    # Implement your SMS sending logic here
    # For example, using an external API
    api_url = "https://sms.nalosolutions.com/smsbackend/Resl_Nalo/send-message/"
    api_key = 'aamecjsju58x!shnojyy9yhj4f!d)0!j2n1hs9cj2ityto2pf3qcs2oc2at@ryb1'
    payload = {
        'phone_number': phone_number,
        'message': message,
        'api_key': api_key
    }
    response = requests.post(api_url, data=payload)
    return response.status_code == 200