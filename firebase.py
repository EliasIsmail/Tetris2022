import firebase_admin
from firebase_admin import credentials, db
import os

db_url = 'https://tetris-7eac9-default-rtdb.europe-west1.firebasedatabase.app'

cred = credentials.Certificate("tetris-7eac9-firebase-adminsdk-7iimv-71ce654bec.json")
firebase_admin.initialize_app(cred, {'databaseURL':db_url})

ref = db.reference("/")