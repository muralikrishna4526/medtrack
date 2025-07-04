import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.create_table(
    TableName='Appointments',
    KeySchema=[
        {'AttributeName': 'appointment_id', 'KeyType': 'HASH'},  # Partition key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'appointment_id', 'AttributeType': 'S'},
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print("Creating Appointments table...")
table.meta.client.get_waiter('table_exists').wait(TableName='Appointments')
print("✅ Table created successfully.")