resource "aws_dynamodb_table" "registrations" {

  name = "${var.project_name}-registrations"

  billing_mode = "PAY_PER_REQUEST"

  hash_key = "registration_id"

  attribute {
    name = "registration_id"
    type = "S"
  }

  attribute {
    name = "event_id"
    type = "S"
  }

  global_secondary_index {
    name            = "EventIndex"
    hash_key        = "event_id"
    projection_type = "ALL"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}