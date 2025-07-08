##########################################################################
################## FEARLESS-BIRDS S3-BUCKETS #############################
##########################################################################

##### Create S3 Buckets for fearless-birds
resource "aws_s3_bucket" "fearless-birds-buckets" {
  count = length(var.fearless_birds_buckets)
  bucket = "${var.fearless_birds_buckets[count.index]}"         #"fearless-birds-buckets"
  tags = var.tags
}