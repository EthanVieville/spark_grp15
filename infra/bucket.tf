resource "aws_s3_bucket" "bucket" {
  bucket = "ethan-bucket-mayer-sdibr"

  tags = local.tags
}