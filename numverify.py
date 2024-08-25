import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv('API_KEY')
41764890243

def validate_number(phone):
    url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={phone}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        result = response.json()
        
        if result.get("valid"):
            return True
        else:
            print(f"Invalid phone number: {phone}. Error: {result.get('error', {}).get('info', 'No error info available.')}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête API: {e}")
        return False
