# Download the helper library from https://www.twilio.com/docs/python/install
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# message = client.messages.create(
#                               to='whatsapp:+2348135810804',
#                               body='Hello there!',
#                               from_='whatsapp:+14155238886',
#                           )

# print(message.sid)
message = "Testing Message"
to_number = "+2348135810804"
def send_message(message, to_number):
    try:
        from_number = os.environ["TWILIO_NUMBER"]
        # Use the Twilio API to send a WhatsApp message
        bot_message = client.messages.create(
            to=f"whatsapp:{to_number}",  # The recipient's WhatsApp number
            from_=f"whatsapp:{from_number}",  # Your Twilio WhatsApp number
            body=message,  # The message you want to send
        )
        # print(bot_message)
        print({"message": "WhatsApp message sent successfully"})
    except Exception as e:
        raise Exception("error:" + str(e))

response = send_message(message, to_number)