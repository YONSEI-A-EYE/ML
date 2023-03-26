import os
import firebase_admin
from firebase_admin import credentials


def fcm_conf():
    current_working_directory = os.getcwd()
    cred = credentials.Certificate(f"{current_working_directory}/app/fcm-secret.json")
    firebase_admin.initialize_app(cred)
