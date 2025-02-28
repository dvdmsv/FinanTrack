import os
import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        'mysql+pymysql://dvdmsv:finantrack@dvdmsv.mysql.pythonanywhere-services.com/dvdmsv$finanzas'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_urlsafe(64)
    CORS_ORIGINS = ["http://localhost", "http://localhost:4200"]
    METHODS = ["GET", "POST", "OPTIONS", "DELETE", "PATCH"]
    HEADERS = ["Content-Type", "Authorization"]
