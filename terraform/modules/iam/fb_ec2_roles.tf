################################################################
################## FEARLESS-BIRDS IAM ##########################
################################################################


#####------------------------------------#####
#####           FB-EC2-TEST-ROLE         #####
#####------------------------------------#####
data "aws_iam_policy_document" "instance_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service" 
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "inline_policy" {
  statement {
    actions   = ["ec2:DescribeAccountAttributes"]
    resources = ["*"]
  }
}

resource "aws_iam_role" "fb-ec2-role" {
  name               = "fb-ec2-test-role"
  assume_role_policy = data.aws_iam_policy_document.instance_assume_role_policy.json 

  inline_policy {
    name = "fb_ec2_inline_policy_2"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["ec2:Describe*"]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
    })
  }

  inline_policy {
    name   = "fb_ec2_inline_policy_1"
    policy = data.aws_iam_policy_document.inline_policy.json
  }
}



#####--------------------------------------#####
#####           FB-EC2-SURVEY-ROLE         #####
#####--------------------------------------#####




