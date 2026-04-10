import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "meet-sphere-secret-key"

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_EMAIL = "your_email@gmail.com"
    SMTP_PASSWORD = "your_app_password"