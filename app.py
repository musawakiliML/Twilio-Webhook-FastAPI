from fastapi import FastAPI, Form, Response, Request, HTTPException, status
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from dotenv import load_dotenv
import os

load_dotenv()

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