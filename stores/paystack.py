import requests
from django.conf import settings

class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co"
    
    def verify_payment(self,ref,*args,**kwargs):
        path = f'/transaction/verify/{ref}'
        headers = {
            "authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "content-type": "application/json",
            "cache-control": "no-cache"
        }
        url = self.base_url+path
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("data"):
                return True, response_data['data']
            return False, response_data.get("Message","No data found")
        return False, "Failed to verify payment"