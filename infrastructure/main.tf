terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-2"
}

data "aws_iam_policy_document" "lambda_policy_document" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_policy_document.json
}

resource "aws_lambda_function" "parse_pages_lambda" {
  function_name = "parse_pages"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.handler"
  filename      = "default_handler.zip"

  runtime = "python3.10"
}

resource "aws_lambda_function" "get_all_hoods_lambda" {
  function_name = "get_all_hoods"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.handler"
  filename      = "default_handler.zip"

  runtime = "python3.10"
}


