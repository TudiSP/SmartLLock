import datetime

from django.contrib.sessions.models import Session

from SmartLLock.settings import QR_TTL
import uuid


def generate_code():
    token = uuid.uuid1()
    return token.hex


def isValid(code):
    for session_raw in Session.objects.all():
        session = session_raw.get_decoded()
        if 'Datetime' not in session.keys():
            continue
        session_t = datetime.datetime.fromisoformat(session['Datetime']).time()
        session_seconds = (session_t.hour * 60 + session_t.minute) * 60 + session_t.second
        present_t = datetime.datetime.now().time()
        present_seconds = (present_t.hour * 60 + present_t.minute) * 60 + present_t.second
        elapsed_seconds = present_seconds - session_seconds

        print(f"Deltatime: {elapsed_seconds}")
        if elapsed_seconds <= QR_TTL:
            print(f"Session code: {session['Code']}, unvalidated code: {code}")
            if session['Code'] == int(code):
                print('OK')
                return True
    return False
