#!/bin/bash

# Test script for ShortURL Service (using curl only)

BASE_URL=http://127.0.0.1:8000

# 1. Create a new short URL
echo "1. Creating a new short URL..."
RESPONSE=$(curl -s -X POST $BASE_URL/shorten -H "Content-Type: application/json" -d '{"url": "https://example.com"}')

if [[ $RESPONSE == *"short_id"* ]]; then
    echo "Response: $RESPONSE"
    SHORT_ID=$(echo $RESPONSE | grep -o '"short_id":"[^"]*"' | cut -d':' -f2 | tr -d '"')
    echo "Short ID: $SHORT_ID"
else
    echo "Error: Failed to create short URL. Response: $RESPONSE"
    exit 1
fi

# 2. Retrieve the original URL using the short ID
echo "2. Retrieving original URL..."
REDIRECT_RESPONSE=$(curl -s $BASE_URL/$SHORT_ID)

if [[ $REDIRECT_RESPONSE == *"original_url"* ]]; then
    echo "Redirect Response: $REDIRECT_RESPONSE"
else
    echo "Error: Failed to retrieve original URL. Response: $REDIRECT_RESPONSE"
    exit 1
fi

# 3. Confirm the redirect is correct
EXPECTED_URL="https://example.com"
ACTUAL_URL=$(echo $REDIRECT_RESPONSE | grep -o '"original_url":"[^"]*"' | cut -d':' -f2- | tr -d '"' | sed 's:/*$::')

if [[ "$ACTUAL_URL" == "$EXPECTED_URL" ]]; then
    echo "Test Passed: Redirect works correctly."
else
    echo "Test Failed: Redirect does not work as expected."
    echo "Expected: $EXPECTED_URL"
    echo "Got: $ACTUAL_URL"
    exit 1
fi

echo "All tests passed."
