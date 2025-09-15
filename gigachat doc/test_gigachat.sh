#!/bin/bash

# GigaChat API Test Script
# This script tests your GigaChat credentials by:
# 1. Getting an authentication token
# 2. Fetching available models
# 3. Sending a test chat message

# Load credentials from GigaChatApi.txt file
if [ ! -f "GigaChatApi.txt" ]; then
    echo -e "${RED}Error: GigaChatApi.txt file not found${NC}"
    echo "Please create a GigaChatApi.txt file with your credentials in the format:"
    echo "Client ID: your_client_id"
    echo "Scope: GIGACHAT_API_PERS"
    echo "Authorization Key: your_base64_encoded_key"
    exit 1
fi

# Parse credentials from file
CLIENT_ID=$(grep "^Client ID:" GigaChatApi.txt | cut -d':' -f2- | xargs)
SCOPE=$(grep "^Scope:" GigaChatApi.txt | cut -d':' -f2- | xargs)
AUTH_KEY=$(grep "^Authorization Key:" GigaChatApi.txt | cut -d':' -f2- | xargs)

BASE_URL="https://gigachat.devices.sberbank.ru/api/v1"
AUTH_URL="https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== GigaChat API Test Script ===${NC}"
echo

# Check if credentials are set
if [ "$CLIENT_ID" = "YOUR_CLIENT_ID_HERE" ] || [ "$CLIENT_SECRET" = "YOUR_CLIENT_SECRET_HERE" ]; then
    echo -e "${RED}Error: Please set your CLIENT_ID and CLIENT_SECRET in this script${NC}"
    echo "Edit this file and replace YOUR_CLIENT_ID_HERE and YOUR_CLIENT_SECRET_HERE with your actual credentials"
    exit 1
fi

# Step 1: Get authentication token
echo -e "${YELLOW}Step 1: Getting authentication token...${NC}"

# Create base64 encoded credentials
CREDENTIALS=$(echo -n "$CLIENT_ID:$CLIENT_SECRET" | base64)

# Generate UUID for RqUID
RQUID=$(uuidgen)

TOKEN_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "$AUTH_URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -H "RqUID: $RQUID" \
  -H "Authorization: Basic $CREDENTIALS" \
  -d "scope=GIGACHAT_API_PERS")

# Extract HTTP status code and response body
HTTP_CODE=$(echo "$TOKEN_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$TOKEN_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓ Authentication successful${NC}"
    ACCESS_TOKEN=$(echo "$RESPONSE_BODY" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo "Access token received (first 20 chars): ${ACCESS_TOKEN:0:20}..."
    echo
else
    echo -e "${RED}✗ Authentication failed (HTTP $HTTP_CODE)${NC}"
    echo "Response: $RESPONSE_BODY"
    exit 1
fi

# Step 2: Get available models
echo -e "${YELLOW}Step 2: Getting available models...${NC}"

MODELS_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X GET "$BASE_URL/models" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json")

# Extract HTTP status code and response body
HTTP_CODE=$(echo "$MODELS_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$MODELS_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓ Models retrieved successfully${NC}"
    echo "Available models:"
    echo "$RESPONSE_BODY" | python3 -m json.tool | grep '"id"' | head -5
    
    # Extract first model ID for chat test
    FIRST_MODEL=$(echo "$RESPONSE_BODY" | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)
    echo "Using model for chat test: $FIRST_MODEL"
    echo
else
    echo -e "${RED}✗ Failed to get models (HTTP $HTTP_CODE)${NC}"
    echo "Response: $RESPONSE_BODY"
    exit 1
fi

# Step 3: Send a test chat message
echo -e "${YELLOW}Step 3: Sending test chat message...${NC}"

CHAT_REQUEST='{
  "model": "'$FIRST_MODEL'",
  "messages": [
    {
      "role": "user",
      "content": "Привет! Как дела?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 100
}'

CHAT_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$CHAT_REQUEST")

# Extract HTTP status code and response body
HTTP_CODE=$(echo "$CHAT_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$CHAT_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓ Chat message sent successfully${NC}"
    echo "Model response:"
    echo "$RESPONSE_BODY" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print('  Message:', data['choices'][0]['message']['content'])
    print('  Tokens used:', data['usage']['total_tokens'])
except Exception as e:
    print('Error parsing response:', e)
    "
    echo
else
    echo -e "${RED}✗ Failed to send chat message (HTTP $HTTP_CODE)${NC}"
    echo "Response: $RESPONSE_BODY"
    exit 1
fi

echo -e "${GREEN}=== All tests completed successfully! ===${NC}"
echo -e "${BLUE}Your GigaChat credentials are working correctly.${NC}"