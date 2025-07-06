import boto3

# Connect to DynamoDB in your region
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Create the Diagnoses table
table = dynamodb.create_table(
    TableName='Diagnoses',
    KeySchema=[
        {'AttributeName': 'diagnosis_id', 'KeyType': 'HASH'}  # Partition key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'diagnosis_id', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print("🩺 Creating Diagnoses table...")
table.meta.client.get_waiter('table_exists').wait(TableName='Diagnoses')
print("✅ Diagnoses table created successfully!")