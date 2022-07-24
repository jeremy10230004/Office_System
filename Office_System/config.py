import firebase_admin
from firebase_admin import credentials


def firebase_init():
    cred = credentials.Certificate(secret_key_json)
    firebase_admin.initialize_app(cred)


secret_key_json = "!!YOUR FIREBASE SECRET KEY!!"
