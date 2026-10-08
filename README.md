# Serverless Image Resizer using AWS

## Project Objective

The objective of this project is to build a serverless image processing system that automatically resizes images uploaded to Amazon S3.

The project uses Amazon S3, AWS Lambda, API Gateway, IAM, and CloudWatch to create a secure and automated image resizing workflow.

---

## AWS Services Used

* **Amazon S3** – Stores original and resized images.
* **AWS Lambda** – Processes and resizes uploaded images using Python and Pillow.
* **Amazon API Gateway** – Provides an API endpoint for requesting a secure upload URL.
* **AWS IAM** – Provides required permissions to Lambda functions.
* **Amazon CloudWatch** – Used for Lambda monitoring and logs.

---

## Architecture / Workflow

The application follows this workflow:

```text
User
  ↓
Frontend (HTML, CSS, JavaScript)
  ↓
API Gateway
  ↓
Upload API Lambda
  ↓
Presigned S3 Upload URL
  ↓
Original S3 Bucket
  ↓
S3 Object Created Event
  ↓
ImageResizerFunction Lambda
  ↓
Pillow Image Processing
  ↓
Resized S3 Bucket
```

### S3 Buckets

**Original Image Bucket**

`image-resizer-original-12345`

**Resized Image Bucket**

`image-resizer-resized-rutuja123`

---

## Project Structure

```text
serverless-image-resizer/
│
├── index.html
├── style.css
├── script.js
├── lambda_function.py
├── upload_api.py
├── README.md
├── .gitignore
├── architecture-diagram.png
│
└── screenshots/
    ├── s3-original-upload.png
    ├── s3-resized-image.png
    ├── lambda-function.png
    ├── api-gateway-route.png
    └── upload-api-lambda.png
```

---

## Implementation Steps

### 1. Create the S3 Buckets

Two S3 buckets were created:

* `image-resizer-original-12345`
* `image-resizer-resized-rutuja123`

The first bucket stores original uploaded images and the second bucket stores resized images.

---

### 2. Create the Image Resizer Lambda

An AWS Lambda function named:

`ImageResizerFunction`

was created using Python 3.12.

The Lambda function:

1. Receives an S3 upload event.
2. Reads the uploaded image from the original bucket.
3. Uses the Pillow library to process the image.
4. Resizes the image to fit within `800 × 800` pixels.
5. Uploads the resized image to the resized S3 bucket.

The Lambda function uses a Pillow Lambda Layer.

---

### 3. Configure IAM Permissions

An IAM role named:

`ImageResizerLambdaRole`

was used by the image processing Lambda.

The required S3 permissions allow the function to:

* Read objects from the original S3 bucket.
* Write processed objects to the resized S3 bucket.

---

### 4. Configure S3 Event Trigger

An S3 Object Created event was configured on:

`image-resizer-original-12345`

Whenever a new image is uploaded, S3 automatically invokes:

`ImageResizerFunction`

---

### 5. Create Upload API Lambda

A second Lambda function named:

`ImageResizerUploadAPI`

was created.

Its purpose is to generate a temporary S3 presigned URL.

The URL allows the frontend to upload an image directly to the original S3 bucket without exposing AWS credentials.

---

### 6. Configure API Gateway

An HTTP API named:

`ImageResizerUploadAPI`

was created.

Route:

```text
POST /upload
```

API endpoint:

```text
https://tnb6qmmsi2.execute-api.ap-south-1.amazonaws.com/upload
```

The API Gateway route invokes the `ImageResizerUploadAPI` Lambda function.

---

### 7. Create the Frontend

A simple frontend was created using:

* HTML
* CSS
* JavaScript

The user selects an image and clicks:

**Upload & Resize**

The JavaScript application:

1. Sends a POST request to API Gateway.
2. Receives the presigned S3 upload URL.
3. Uploads the selected image directly to S3.
4. S3 triggers the image processing Lambda.
5. The resized image is stored in the resized bucket.

---

### 8. Configure CORS

CORS was configured for API Gateway and the S3 bucket so that the local frontend can communicate with the AWS services.

The frontend was tested using VS Code Live Server.

---

## Image Processing

The image processing is performed using the Pillow Python library.

The image is resized while maintaining its aspect ratio:

```python
image.thumbnail((800, 800))
```

The processed image is then stored under the:

```text
resized/
```

prefix in the resized S3 bucket.

---

## Screenshots

### Original Image Uploaded to S3

![Original S3 Upload](screenshots/s3-original-upload.png)

### Resized Image in S3

![Resized Image](screenshots/s3-resized-image.png)

### Image Resizer Lambda

![Image Resizer Lambda](screenshots/lambda-function.png)

### API Gateway Route

![API Gateway Route](screenshots/api-gateway-route.png)

### Upload API Lambda

![Upload API Lambda](screenshots/upload-api-lambda.png)

---

## How to Run / Test

### Step 1: Open the Project

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/serverless-image-resizer.git
```

Open the project folder.

### Step 2: Start the Frontend

Open the project using VS Code and run `index.html` using Live Server.

The application opens locally, for example:

```text
http://127.0.0.1:5500/index.html
```

### Step 3: Upload an Image

1. Select an image.
2. Click **Upload & Resize**.
3. The frontend requests a presigned URL from API Gateway.
4. The image is uploaded to the original S3 bucket.
5. S3 automatically triggers the Lambda function.
6. Lambda resizes the image.
7. The resized image is stored in the resized S3 bucket.

### Step 4: Verify the Output

Open:

```text
image-resizer-resized-rutuja123
```

and check the:

```text
resized/
```

folder.

---

## Security

* AWS credentials are not stored in the frontend.
* The frontend uses an S3 presigned URL for uploading.
* IAM permissions are provided through Lambda execution roles.
* S3 access is restricted to the required actions.
* AWS credentials and sensitive files are excluded using `.gitignore`.
* No AWS access keys or secret keys are uploaded to GitHub.

---

## Error Handling and Monitoring

AWS Lambda execution logs can be monitored using Amazon CloudWatch.

If image processing fails, Lambda execution logs can be checked to identify errors such as:

* Invalid image files
* S3 permission errors
* Missing objects
* Image processing errors
* Lambda execution errors

---

## Key Learnings

Through this project, I learned:

* How S3 event notifications trigger Lambda functions.
* How to process files using AWS Lambda.
* How to use Pillow for image processing.
* How to create and use S3 presigned URLs.
* How API Gateway communicates with Lambda.
* How IAM roles provide secure AWS permissions.
* How CORS works between a frontend and AWS services.
* How to monitor Lambda functions using CloudWatch.
* How serverless services can be combined to create an automated workflow.

---

## Possible Improvements

The project can be improved further by:

* Supporting multiple image formats.
* Allowing users to select the resize dimensions.
* Adding authentication to the API.
* Adding a frontend preview of the resized image.
* Adding image status tracking.
* Using CloudFront for faster image delivery.
* Adding stronger validation for uploaded files.
* Adding automated deployment using AWS SAM or Terraform.

---

## Conclusion

This project demonstrates a complete serverless image processing workflow using AWS.

An image uploaded through the frontend is securely sent to Amazon S3, automatically processed by AWS Lambda, resized using Pillow, and stored in a separate S3 location.

The project demonstrates how AWS managed and serverless services can work together without maintaining traditional servers.

---

## Author

**Rutuja Dandawate**

AWS Capstone Project – Serverless Image Resizer
