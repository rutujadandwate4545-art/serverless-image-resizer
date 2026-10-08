import boto3
import io
from PIL import Image
from urllib.parse import unquote_plus

s3 = boto3.client("s3")

OUTPUT_BUCKET = "image-resizer-resized-rutuja123"

def lambda_handler(event, context):
    record = event["Records"][0]

    source_bucket = record["s3"]["bucket"]["name"]
    source_key = unquote_plus(record["s3"]["object"]["key"])

    response = s3.get_object(
        Bucket=source_bucket,
        Key=source_key
    )

    image_data = response["Body"].read()
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail((800, 800))

    output = io.BytesIO()
    image_format = image.format if image.format else "JPEG"
    image.save(output, format=image_format)
    output.seek(0)

    output_key = "resized/" + source_key

    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=output_key,
        Body=output,
        ContentType=response.get("ContentType", "image/jpeg")
    )

    return {
        "statusCode": 200,
        "message": "Image resized successfully",
        "output": output_key
    }
