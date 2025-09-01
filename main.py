import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, messaging

app = FastAPI()

# نقرأ بيانات الـ Service Account من متغير بيئة
service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")

if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(service_account_json))
    firebase_admin.initialize_app(cred)

class NotificationData(BaseModel):
    token: str
    title: str
    body: str

@app.get("/")
def root():
    return {"message": "Firebase Notification API is running 🚀"}

@app.post("/send-notification")
def send_notification(data: NotificationData):
    message = messaging.Message(
        notification=messaging.Notification(
            title=data.title,
            body=data.body,
        ),
        token=data.token,
    )
    response = messaging.send(message)
    return {"status": "success", "message_id": response}
