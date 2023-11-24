import json
from decimal import Decimal
import boto3
from botocore.exceptions import NoCredentialsError

# AWS credentials
aws_access_key_id = 'xxxxxxxxxxxxxxxx'
aws_secret_access_key = 'xxxxxxxxxxx'
aws_region = 'xxxxxxxxxxxxxx'
table_name = 'xxxxxxxxxxx'

# Set up DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

table = dynamodb.Table(table_name)

# Function to convert Decimal to a serializable format
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)  # Convert Decimal to string
    raise TypeError(f'Type {type(obj)} is not JSON serializable')

# Function to export DynamoDB data to JSON
def export_dynamodb_to_json():
    try:
        items = []
        last_evaluated_key = None

        while True:
            # Scan DynamoDB table and get a page of items
            response = table.scan(ExclusiveStartKey=last_evaluated_key) if last_evaluated_key else table.scan()
            items.extend(response['Items'])

            # Check if there are more items to fetch
            last_evaluated_key = response.get('LastEvaluatedKey')
            if not last_evaluated_key:
                break

        # Convert items to JSON with custom encoder
        json_data = json.dumps(items, indent=2, default=decimal_default)

        # Save JSON data to a file
        output_file_path = 'dynamodb_data.json'
        with open(output_file_path, 'w') as output_file:
            output_file.write(json_data)

        print(f'Data exported to {output_file_path}')

    except NoCredentialsError:
        print('Credentials not available')

# Call the function
export_dynamodb_to_json()

