import os
import firebase_admin
from firebase_admin import credentials
# from google.cloud import secretmanager


def fcm_conf():
    current_working_directory = os.getcwd()
    cred = credentials.Certificate(f"{current_working_directory}/fcm-secret.json")
    firebase_admin.initialize_app(cred)
