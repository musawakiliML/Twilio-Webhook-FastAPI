from fastapi import FastAPI, Form, Response, Request, HTTPException, status
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

app = FastAPI()

@app.post("/hook")
async def chat(request: Request, From: str = Form(...), Body: str = Form(...)):
    
    validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])
    form_ = await request.form()
    if not validator.validate(str(request.url), form_, request.headers.get("X-Twilio-Signature", "")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in Twilio Signature")

    response = MessagingResponse()
    msg = response.message(f"Hi {From}, you said: {Body}")
    return Response(content=str(response), media_type="application/xml")

@app.post("/whatsapp")
async def receive_message(request: Request):
    try:
        request_body = await request.form()
        print(request_body)
        message_test = "Test"
        response = send_message("+2348135810804", message_test)
        # raise Exception("Message processed and replied with translation.")
        return str(response)
    except Exception as e:
        raise Exception("An error occurred: " + str(e))

def send_message(to_number, message):
    try:
        from_number = os.environ["TWILIO_NUMBER"]
        # Use the Twilio API to send a WhatsApp message
        bot_message = client.messages.create(
            to=f"whatsapp:{to_number}",  # The recipient's WhatsApp number
            from_=f"whatsapp:{from_number}",  # Your Twilio WhatsApp number
            body=message,  # The message you want to send
        )
        print(bot_message)
        return {"message": "WhatsApp message sent successfully"}
    except Exception as e:
        return {"error": str(e)}