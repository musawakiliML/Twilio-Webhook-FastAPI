from fastapi import FastAPI, Form, Response, Request, HTTPException
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from pydotenv import 

app = FastAPI()

@app.post("/hook")
async def chat(request: Request, From: str = Form(...), Body: str = Form(...)):
    
    validator = RequestValidator
    
    response = MessagingResponse()
    msg = response.message(f"Hi {From}, you said: {Body}")
    return Response(content=str(response), media_type="application/xml")