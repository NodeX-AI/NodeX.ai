import requests
import sys
from config.config import *

def test_upload():
    test_image = b'test_image_data' * 1000
    
    files = {'source': ('test.jpg', test_image, 'image/jpeg')}
    data = {
        'key': IMAGE_HOSTING_KEY,
        'action': 'upload', 
        'format': 'json'
    }
    
    response = requests.post(IMAGE_HOSTING_URL, files=files, data=data, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"URL: {result.get('image', {}).get('url')}")

if __name__ == "__main__":
    test_upload()