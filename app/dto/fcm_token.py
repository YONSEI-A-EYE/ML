from pydantic import BaseModel


class FCMToken(BaseModel):
    token: str
