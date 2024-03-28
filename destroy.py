import boto3

# Configure AWS credentials
aws_access_key_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
aws_secret_access_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
aws_region = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"  # For example, "us-east-1"

# Name of the table to delete data from
table_name = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
  
# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)


# Get the primary key attribute name(s) from the table's KeySchema
response = dynamodb.describe_table(TableName=table_name)
key_attributes = [key['AttributeName'] for key in response['Table']['KeySchema']]

# Scan and delete all items in the table using transact_write_items
def delete_all_items():
    response = dynamodb.scan(TableName=table_name)

    items_to_delete = []

    for item in response['Items']:
        key = {k: v for k, v in item.items() if k in key_attributes}
        items_to_delete.append({'Delete': {'TableName': table_name, 'Key': key}})
        print(f"Queued item for deletion: {key}")

    # Batch write to delete items using transact_write_items
    while items_to_delete:
        batch_size = min(25, len(items_to_delete))  # transact_write_items has a limit of 25 items per request
        batch_items, items_to_delete = items_to_delete[:batch_size], items_to_delete[batch_size:]

        transact_request = [{'Delete': item['Delete']} for item in batch_items]
        dynamodb.transact_write_items(TransactItems=transact_request)

        print(f"Deleted {batch_size} items")

if __name__ == '__main__':
    delete_all_items()
