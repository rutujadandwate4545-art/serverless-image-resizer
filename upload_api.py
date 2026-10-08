import json
import boto3
import uuid

s3 = boto3.client("s3")

BUCKET_NAME = "image-resizer-original-12345"

def lambda_handler(event, context):

    file_name = "upload-" + str(uuid.uuid4()) + ".jpg"

    upload_url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": file_name,
            "ContentType": "image/jpeg"
        },
        ExpiresIn=300
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps({
            "upload_url": upload_url,
            "file_name": file_name
        })
    }