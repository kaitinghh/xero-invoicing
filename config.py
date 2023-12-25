import secrets

class Config:
    STATE = secrets.token_urlsafe(16)
    SECRET_KEY = secrets.token_hex(16)
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = 'flask_session'
    SERVER_NAME = 'localhost:3000'
