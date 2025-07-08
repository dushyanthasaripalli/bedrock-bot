

# IAM Role for Glue Job
resource "aws_iam_role" "glue_role" {
  name = "fb-glue-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# S3 and Glue Job Policy
resource "aws_iam_policy" "glue_s3_policy" {
  name        = "glue-s3-policy"
  description = "IAM policy for Glue job to access S3"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::${var.fb_results_bucket}",
        "arn:aws:s3:::${var.fb_results_bucket}/*",
        "*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetJob",
        "glue:StartJobRun",
        "glue:GetJobRun",
        "glue:GetJobRuns"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF
}

# DynamoDB Access Policy
resource "aws_iam_policy" "dynamodb_policy" {
  name        = "glue-dynamodb-policy"
  description = "IAM policy for Glue job to access DynamoDB"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:BatchGetItem",
        "dynamodb:BatchWriteItem",
        "dynamodb:DescribeTable",
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": "arn:aws:dynamodb:${var.region}:${var.account_id}:table/*"
    }
  ]
}
EOF
}

# Attach Policies to Role
resource "aws_iam_role_policy_attachment" "glue_s3_attach" {
  role       = aws_iam_role.glue_role.name
  policy_arn = aws_iam_policy.glue_s3_policy.arn
}

resource "aws_iam_role_policy_attachment" "glue_dynamodb_attach" {
  role       = aws_iam_role.glue_role.name
  policy_arn = aws_iam_policy.dynamodb_policy.arn
}

# Output the IAM Role ARN
output "glue_role_arn" {
  value = aws_iam_role.glue_role.arn
}
