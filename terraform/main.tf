#########################################################
#####------ Main Terraform Configuration File ------#####
#########################################################

provider "aws" {
  region = "us-east-1"
}

### Create an S3 bucket
resource "aws_s3_bucket" "react_site" {
  bucket        = "cappy-ai-react-site-bucket"  # ⚠️ MUST be globally unique
  force_destroy = true
}

### Enable static website hosting
resource "aws_s3_bucket_website_configuration" "react_site" {
  bucket = aws_s3_bucket.react_site.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}

# Allow public access to the bucket
resource "aws_s3_bucket_public_access_block" "allow_public" {
  bucket = aws_s3_bucket.react_site.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Bucket policy to allow public read of all files
resource "aws_s3_bucket_policy" "public_policy" {
  bucket = aws_s3_bucket.react_site.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = "*",
      Action    = "s3:GetObject",
      Resource  = "${aws_s3_bucket.react_site.arn}/*"
    }]
  })
}

# Upload React build files from ../frontend/build
resource "aws_s3_object" "react_files" {
  for_each = fileset("${path.module}/../frontend/build", "**/*")

  bucket = aws_s3_bucket.react_site.id
  key    = each.value
  source = "${path.module}/../frontend/build/${each.value}"
  etag   = filemd5("${path.module}/../frontend/build/${each.value}")

  content_type = lookup({
    html = "text/html"
    js   = "application/javascript"
    css  = "text/css"
    png  = "image/png"
    jpg  = "image/jpeg"
    svg  = "image/svg+xml"
    json = "application/json"
    ico  = "image/x-icon"
    txt  = "text/plain"
  }, split(".", each.value)[length(split(".", each.value)) - 1], "application/octet-stream")
}


output "build_files" {
  value = fileset("${path.module}/../frontend/build", "**/*")
}

# Output the public website URL
output "website_url" {
  value = aws_s3_bucket_website_configuration.react_site.website_endpoint
}



##### Module VPC
# module cappy-ai-vpc{
#     source                    = "./modules/vpc"
# }

# ##### Module IAM
# module cappy-ai-iam{
#     source                    = "./modules/iam"
#     ou                        = var.ou
#     tags                      = var.tags
#     region                    = var.region
#     account_id                = var.account_id
#     fb_results_bucket         = var.fb_results_bucket
#     fb_scripts_bucket         = var.fb_scripts_bucket   
# }

# An example resource that does nothing.
resource "null_resource" "example" {
    triggers = {
    value = "A example resource that does nothing!"
    }
}

# resource "null_resource" "example2" {
#     triggers = {
#     value = "A example resource that does nothing!"
#     }
# }

# #### Module S3
# module cappy-ai-s3{
#     source                    = "./modules/s3"
#     ou                        = var.ou
#     acl                       = var.acl
#     tags                      = var.tags
#     region                    = var.region
#     account_id                = var.account_id
#     fearless_birds_buckets    = var.fearless_birds_buckets
#     fb_scripts_bucket         = var.fb_scripts_bucket
#     fb_scripts_bucket_files   = var.fb_scripts_bucket_files
# }

# ##### Module Glue
# module cappy-ai-glue{
#     source                    = "./modules/glue"
#     glue_etl_role_arn         = module.cappy-ai-iam.glue_role_arn
#     tags                      = var.tags
#     s3_script_bucket          = var.fb_scripts_bucket
#     ou                        = var.ou
#     s3_results_bucket         = var.fb_results_bucket
#     region                    = var.region
#     rs_account_id_clm         = var.rs_account_id_clm
#     rs_cluster_id_clm         = var.rs_cluster_id_clm
#     rs_db_clm                 = var.rs_db_clm
#     rs_db_user_clm            = var.rs_db_user_clm
#     rs_edla_role_clm          = var.rs_edla_role_clm
# }