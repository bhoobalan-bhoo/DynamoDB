import boto3

# Configure AWS credentials
aws_access_key_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
aws_secret_access_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
region_name = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"  # For example, "us-east-1"

# Name of the table to delete data from
table_name = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
  
# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)


# Get the primary key attribute name(s) from the table's KeySchema
response = dynamodb.describe_table(TableName=table_name)
key_attributes = [key['AttributeName'] for key in response['Table']['KeySchema']]

# Scan and delete all items in the t    able
def delete_all_items():
    response = dynamodb.scan(TableName=table_name)

    for item in response['Items']:
        key = {k: v for k, v in item.items() if k in key_attributes}
        dynamodb.delete_item(TableName=table_name, Key=key)
        print(f"Deleted item: {key}")

    while 'LastEvaluatedKey' in response:
        response = dynamodb.scan(TableName=table_name, ExclusiveStartKey=response['LastEvaluatedKey'])

        for item in response['Items']:
            key = {k: v for k, v in item.items() if k in key_attributes}
            dynamodb.delete_item(TableName=table_name, Key=key)
            print(f"Deleted item: {key}")

if __name__ == '__main__':
    delete_all_items()
