import json
import boto3
import os

def validate_parameters(event):
  errors  = []

  if not event.get("name"):
    errors.append("name key is required")
  elif not event["name"]:
    errors.append("name cannot be blank")

  if not event.get("email"):
    errors.append("email key is required")
  elif not event["email"]:
    errors.append("email cannot be blank")

  if not event.get("message"):
    errors.append("message key is required")
  elif not event["message"]:
    errors.append("message cannot be blank")

  return errors

def lambda_handler(event, context):
  """
  Parameters
  ----------
  event: dict, required
      API Gateway Lambda Proxy Input Format

      Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

  context: object, required
      Lambda Context runtime methods and attributes

      Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

  Returns
  ------
  API Gateway Lambda Proxy Output Format: dict

      Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
  """

  errors = validate_parameters(event)

  if len(errors) > 0:
    return {
      "statusCode": 401,
      "body": json.dumps({
        "message": "Invalid parameters",
        "errors": errors  
      })
    }
  else:
    name    = event["name"]
    email   = event["email"]
    message = event["message"]

    # Message Parameters
    subject   = "[CB_WEBSITE_MESSAGE] {} - {}".format(name, email)
    topic_arn = "arn:aws:sns:ap-southeast-1:428846808097:CbwebsiteMessenger"

    sns_client  = boto3.client('sns')
    response    = sns_client.publish(
                    TopicArn=topic_arn,
                    Message=message,
                    Subject=subject
                  ) 

    return {
      "statusCode": 200,
      "body": json.dumps({
        "message": "Success!"
      }),
    }
