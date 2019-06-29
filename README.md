> Use opencv with AWS Lambda to do video procession, creating frames and storing it to destination S3 bucket.

## 🚀 Instructions
You can follow the steps below to deploy lambda function. 

1. Create AWS Lambda with `Python 3.7`.

2. Attach role to AWS Lambda with permissions to Source bucket, Destination bucket and DynamoDB table.
e.g. 

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
 	{
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutAccountPublicAccessBlock",
                "s3:GetAccountPublicAccessBlock",
                "s3:ListAllMyBuckets",
                "s3:ListJobs",
                "s3:CreateJob",
                "s3:HeadBucket"
            ],
            "Resource": "*"
        },
	{ 
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::sourcebucket",
                "arn:aws:s3:::sourcebucket/*",
                "arn:aws:s3:::destinationbucket",
                "arn:aws:s3:::destinationbucket/*"
            ]
        },
       	{ 
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGetItem",
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem"
            ],
            "Resource": "dynamodbtable_arn"
        }
    
}

```

**Note**: Make sure you select at least 1 GB of memory and 3-5 minutes of execution time to lambda as video procession takes time. Max video size < 500 MBs and max execution time < 15 minutes.

