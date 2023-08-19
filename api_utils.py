import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('API_KEY')

headers = {
    'X-MBX-APIKEY': api_key,
}