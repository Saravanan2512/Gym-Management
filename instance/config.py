import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://username:password@localhost/gym_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# from dotenv import load_dotenv
# import os

# load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "fallback-key")
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
