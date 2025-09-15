#!/usr/bin/env python3
"""
Test GigaChat file upload functionality
"""

import os
import sys
import requests
import base64
import uuid
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_credentials():
    """Load credentials from GigaChatApi.txt"""
    try:
        with open('/Users/airm1/work/businessaiprocessing/gigachat doc/GigaChatApi.txt', 'r') as f:
            content = f.read()
            
        client_id = None
        auth_key = None
        
        for line in content.strip().split('\n'):
            if line.startswith('Client ID:'):
                client_id = line.split(':', 1)[1].strip()
            elif line.startswith('Authorization Key:'):
                auth_key = line.split(':', 1)[1].strip()
                
        return client_id, auth_key
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return None, None

def get_auth_token(auth_key):
    """Get authentication token"""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json", 
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {auth_key}"
    }
    
    try:
        response = requests.post(
            "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
            headers=headers,
            data={"scope": "GIGACHAT_API_PERS"},
            verify=False
        )
        response.raise_for_status()
        
        token_data = response.json()
        return token_data.get("access_token")
    except Exception as e:
        print(f"Authentication failed: {e}")
        return None

def test_file_upload(access_token):
    """Test file upload with a simple test image"""
    
    # Create a minimal test image (1x1 pixel PNG)
    test_image_data = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    
    headers = {
        "Authorization": f"Bearer {access_token}"
        # Let requests handle Content-Type for multipart
    }
    
    files = {
        "file": ("test.png", test_image_data, "image/png")
    }
    
    data = {
        "purpose": "general"
    }
    
    print("Testing file upload to GigaChat...")
    print(f"File size: {len(test_image_data)} bytes")
    print(f"Headers: {headers}")
    print(f"Data: {data}")
    
    try:
        response = requests.post(
            "https://gigachat.devices.sberbank.ru/api/v1/files",
            headers=headers,
            files=files,
            data=data,
            verify=False
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            file_id = result.get("id")
            print(f"✅ File upload successful! File ID: {file_id}")
            return file_id
        else:
            print(f"❌ File upload failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ File upload error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return None

def main():
    client_id, auth_key = load_credentials()
    if not client_id or not auth_key:
        print("Failed to load credentials")
        sys.exit(1)
    
    print(f"Client ID: {client_id}")
    print(f"Auth Key: {auth_key[:20]}...")
    
    access_token = get_auth_token(auth_key)
    if not access_token:
        print("Failed to get access token")
        sys.exit(1)
    
    print(f"Access token: {access_token[:20]}...")
    
    file_id = test_file_upload(access_token)
    if file_id:
        print(f"Success! File ID: {file_id}")
    else:
        print("File upload test failed")

if __name__ == "__main__":
    main()