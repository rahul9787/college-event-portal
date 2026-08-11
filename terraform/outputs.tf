output "s3_bucket_name" {
  value = aws_s3_bucket.frontend.bucket
}

output "s3_website_endpoint" {
  value = aws_s3_bucket_website_configuration.frontend.website_endpoint
}

output "ecr_repository_url" {
  value = aws_ecr_repository.backend.repository_url
}

output "lambda_function_url" {
  value = var.enable_lambda ? aws_lambda_function_url.backend[0].function_url : null
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.registrations.name
}