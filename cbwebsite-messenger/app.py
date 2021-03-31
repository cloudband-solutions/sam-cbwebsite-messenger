import json
import boto3
import os

def validate_parameters(params):
  errors  = []

  if not params.get("name"):
    errors.append("name cannot be blank")

  if not params.get("email"):
    errors.append("email cannot be blank")

  if not params.get("message"):
    errors.append("message cannot be blank")

  return errors

def lambda_handler(event, context):
  params = None

  if event.get("body"):
    params = json.loads(event.get('body'))

  if params:
    errors = validate_parameters(params)
  else:
    errors = ["no data"]

  if len(errors) > 0:
    return {
      "statusCode": 401,
      'headers': {
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*'
      },
      "body": json.dumps({
        "message": "Invalid parameters",
        "errors": errors  
      })
    }

  name    = params.get('name')
  email   = params.get('email')
  message = params.get('message')

  # Message Parameters
  subject   = "[CB_WEBSITE_MESSAGE] {} - {}".format(name, email)
  topic_arn = os.environ.get("TOPIC_ARN")

  sns_client  = boto3.client('sns')
  response    = sns_client.publish(
                  TopicArn=topic_arn,
                  Message=message,
                  Subject=subject
                ) 

  return {
    "statusCode": 200,
    'headers': {
      'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': '*'
    },
    "body": json.dumps({
      "message": "Success!"
    }),
  }
