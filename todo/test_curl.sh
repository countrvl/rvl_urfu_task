#!/bin/bash

BASE_URL="http://127.0.0.1:8000"

echo "Testing TODO Service Endpoints"

# 1. Create a new task
echo "1. Creating a new task..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/items" \
    -H "Content-Type: application/json" \
    -d '{"title": "Test Task via Curl", "description": "Testing with curl", "completed": false}')
echo "Response: $CREATE_RESPONSE"

# Extract the task ID
TASK_ID=$(echo $CREATE_RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
if [ -z "$TASK_ID" ]; then
    echo "Failed to create task."
    exit 1
fi
echo "Task created with ID: $TASK_ID"

# 2. Get all tasks
echo "2. Retrieving all tasks..."
ALL_TASKS=$(curl -s -X GET "$BASE_URL/items")
echo "Response: $ALL_TASKS"

# 3. Get the created task by ID
echo "3. Retrieving the created task by ID..."
TASK=$(curl -s -X GET "$BASE_URL/items/$TASK_ID")
echo "Response: $TASK"

# 4. Update the task
echo "4. Updating the task..."
UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/items/$TASK_ID" \
    -H "Content-Type: application/json" \
    -d '{"title": "Updated Task via Curl", "description": "Updated via curl", "completed": true}')
echo "Response: $UPDATE_RESPONSE"

# 5. Delete the task
echo "5. Deleting the task..."
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/items/$TASK_ID")
echo "Response: $DELETE_RESPONSE"

# 6. Confirm deletion
echo "6. Confirming deletion..."
CONFIRM_DELETE=$(curl -s -X GET "$BASE_URL/items/$TASK_ID")
echo "Response: $CONFIRM_DELETE"

echo "All tests completed."
