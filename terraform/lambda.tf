resource "aws_lambda_function" "backend" {

  count = var.enable_lambda ? 1 : 0

  function_name = "${var.project_name}-backend"

  role = aws_iam_role.lambda_role.arn

  package_type = "Image"

  image_uri = "${aws_ecr_repository.backend.repository_url}:latest"

  memory_size = 512

  timeout = 30

  environment {
    variables = {
      TABLE_NAME  = aws_dynamodb_table.registrations.name
      ADMIN_TOKEN = var.admin_token
    }
  }

  depends_on = [
    aws_iam_role_policy.lambda_policy
  ]
}


resource "aws_lambda_function_url" "backend" {

  count = var.enable_lambda ? 1 : 0

  function_name = aws_lambda_function.backend[0].function_name

  authorization_type = "NONE"

  cors {
    allow_origins = ["*"]

    allow_methods = [
      "GET",
      "POST",
      "OPTIONS"
    ]

    allow_headers = [
      "Content-Type",
      "X-Admin-Token"
    ]

    max_age = 86400
  }
}