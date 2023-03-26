from fastapi import FastAPI
from firebase_admin import messaging
from dto.fcm_token import FCMToken
from config import fcm_conf
# from utils.fall_detection import baby_monitor
app = FastAPI()
fcm_conf()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/baby/video")
async def baby_monitor_page(token: FCMToken):
    result = baby_monitor()
    if result:
        message = messaging.Message(
            notification=messaging.Notification(
                "Baby had a fall!",
                "CHECK on your baby",
            ),
            token=token.token,
        )
        response = messaging.send(message)
        return response

    return {"message": "baby monitor"}

