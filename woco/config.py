import os
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

ROOT = os.environ.get('ROOT', "") # cloudinary root folder
SITE_URL = os.environ.get('SITE_URL', "") # endpoint for woocommerce
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', "")
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', "")
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', "")
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', "")
WOOCOMMERCE_CONSUMER_KEY = os.environ.get('WOOCOMMERCE_CONSUMER_KEY', "")
WOOCOMMERCE_CONSUMER_SECRET = os.environ.get('WOOCOMMERCE_CONSUMER_SECRET', "")
DEFAULT_LOG_LEVEL = os.environ.get('DEFAULT_LOG_LEVEL', "INFO")
