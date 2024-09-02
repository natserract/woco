import os
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', "")
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', "")
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', "")
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', "")

SITE_NAME = os.environ.get('SITE_NAME', "")
