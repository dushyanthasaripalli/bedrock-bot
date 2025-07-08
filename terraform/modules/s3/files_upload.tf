
## Upload files into FB-SCRIPTS-BUCKET
resource "aws_s3_object" "fearless-birds-scripts-bucket-upload"{
    count = length(var.fb_scripts_bucket_files)
    bucket = "${var.fb_scripts_bucket}"
    acl = var.acl
    key = "tfe_upload/${var.fb_scripts_bucket_files[count.index]}"
    source = "././scripts/fb_scripts/${var.fb_scripts_bucket_files[count.index]}"
    etag = filemd5("././scripts/fb_scripts/${var.fb_scripts_bucket_files[count.index]}")
}