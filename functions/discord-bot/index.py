import os
import json
import boto3

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = os.environ['DISCORD_PUBLIC_KEY']

def handler(event, context):
  print("have event")
  print(event)

  try:
    body = json.loads(event['body'])

    signature = event['headers']['x-signature-ed25519']
    timestamp = event['headers']['x-signature-timestamp']

    # validate the interaction

    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    message = timestamp + json.dumps(body, separators=(',', ':'))

    try:
      verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
    except BadSignatureError:
      return {
          'statusCode': 401,
          'body': json.dumps('invalid request signature')
      }

    # handle the interaction

    t = body['type']

    if t == 1:
      print("Have print")
      return {
          'statusCode': 200,
          'body': json.dumps({
              'type': 1
          })
      }
    elif t == 2:
      print("Have command")
      return command_handler(body)
    else:
      print("Unknown request type")
      return {
          'statusCode': 400,
          'body': json.dumps('unhandled request type')
      }
  except:
    raise


def command_handler(body):
  try:
    command = body['data']['name']

    print(command)
    params = {}
    if 'options' in body['data']:
      for option in body['data']['options']:
        params[option["name"]] = option["value"]

    print(params)

    if command == 'add-ip':
      print("adding ip")
      return build_result(add_ip(**params))
    elif command == 'remove-ip':
      return build_result(remove_ip(**params))
    elif command == 'list-ips':
      return build_result(list_ips())
    else:
      return {
          'statusCode': 400,
          'body': json.dumps('unhandled command')
      }
  except Exception as ex:
    print("Got exception processing request", ex)
    return {
        'statusCode': 400,
        'body': json.dumps('error processing command')
    }

def build_result(object):
  return {
      'statusCode': 200,
      'body': json.dumps({
          'type': 4,
          'data': {
              'content': json.dumps(object),
          }
      })
  }


def add_ip(ip: str):
  return "done"

def remote_ip(ip: str):
  return "done"

def list_ips():
  return ["not", "done", "yet"]

  boto3.client()