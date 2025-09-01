from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# هتحط FCM Server Key في متغير بيئة على Railway
FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY")

class NotificationData(BaseModel):
    token: str      # توكن الجهاز المستقبل
    title: str      # عنوان الإشعار
    body: str       # محتوى الإشعار

@app.get("/")
def root():
    return {"message": "FCM Notification API is running 🚀"}

@app.post("/send-notification")
def send_notification(data: NotificationData):
    if not FCM_SERVER_KEY:
        return {"status": "error", "message": "FCM_SERVER_KEY not set"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"key={FCM_SERVER_KEY}"
    }

    payload = {
        "to": data.token,
        "notification": {
            "title": data.title,
            "body": data.body
        }
    }

    response = requests.post(
        "https://fcm.googleapis.com/fcm/send",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return {"status": "success", "response": response.json()}
    else:
        return {"status": "error", "response": response.text}
