from fastapi import FastAPI, Form, Response, Request, HTTPException, status
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from dotenv import load_dotenv
import os
from twilio.rest import Client
from emoji import emojize

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
        profile_name = request_body.get("ProfileName", "")
        phone_id = request_body.get("WaId", "")
        body = request_body.get("Body", "")
        message_test = welcome_menu(profile_name, "Hi")
        response = send_message("+2348135810804", message_test)
        # raise Exception("Message processed and replied with translation.")
        return str(response)
    except Exception as e:
        raise Exception("An error occurred: " + str(e))

def send_message(to_number, message_text: str):
    try:
        from_number = os.environ["TWILIO_NUMBER"]
        # Use the Twilio API to send a WhatsApp message
        message_text = message_text
        bot_message = client.messages.create(
            to=f"whatsapp:{to_number}",  # The recipient's WhatsApp number
            from_=f"whatsapp:{from_number}",  # Your Twilio WhatsApp number
            body=message_text, # The message you want to send
        )
        return {"message": "WhatsApp message sent successfully"}
    except Exception as e:
        return {"error": str(e)}

def welcome_menu(profile_name: str, start_input: str):
    message = f"{start_input}, {profile_name} Nice to Meet You, I'm EnergiEase Bot {emojize(':bulb:', language='alias')} from Mind Colony!\nWhat would you like to do today? \n\n{emojize(':one:', language='alias')} Buy Electricity⚡\n{emojize(':two:', language='alias')} Customer Support ☎️\n\n Please reply with a number to choose an option(E.g 1 for Buy Electricity)"

    return message