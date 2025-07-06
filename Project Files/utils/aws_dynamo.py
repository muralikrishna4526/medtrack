import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read region and table name from .env
region = os.getenv('AWS_REGION_NAME', 'us-east-1')
users_table_name = os.getenv('USERS_TABLE_NAME', 'Users')

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=region)
users_table = dynamodb.Table(users_table_name)

# Fetch all users (useful for admin or testing)
def load_users():
    response = users_table.scan()
    return response.get('Items', [])

# Register a new user
def register_user(username, password, role):
    users_table.put_item(Item={
        'username': username,
        'password': password,
        'role': role
    })

# Validate login credentials
def validate_login(username, password):
    response = users_table.get_item(Key={'username': username})
    user = response.get('Item')
    if user and user['password'] == password:
        return user['role']
    return None