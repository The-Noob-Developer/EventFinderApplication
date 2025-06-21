import secrets

def getSECRETKEY():
    SECRET_KEY = secrets.token_hex(32)
    return SECRET_KEY