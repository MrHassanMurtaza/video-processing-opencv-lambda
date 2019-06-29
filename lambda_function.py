import cv2
import logging
import os
import boto3
import uuid
from botocore.exceptions import ClientError

DESTINATION_BUCKET=os.environ['BUCKET']
DYNAMO_TABLE=os.environ['TABLE']


s3_resource = boto3.resource('s3')
dynamodb_resource = boto3.resource('dynamodb')
dynamo_table = dynamodb_resource.Table(DYNAMO_TABLE)

def insert_record(file_key, count):
    try:
      dynamo_table.put_item(
        Item={
        'file_name': file_key,
        'count': count
      })
    except ClientError as e:  
      raise Exception("Unexpected dynamo error: %s" % e)

def video_processing(file_key, download_path, destination_bucket):
  vidcap = cv2.VideoCapture(download_path)
  success,image = vidcap.read()
  success = True

  count = 1

  while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC,(int(count)*1000))
    success,image = vidcap.read()
    
    if not success:
      break

    file_name = file_key.split(".")[0] + '%d.jpg' % count
    
    tmp_file_path = '/tmp/' + file_name

    cv2.imwrite(tmp_file_path, image)
    
    print(f'Destination_Path: {tmp_file_path}')
    
    s3_resource.meta.client.upload_file(tmp_file_path, destination_bucket, file_name)

    count = count + 1
  
  # inserting record in dynamodb
  insert_record(file_key, count)

def check_envs():
  if not DESTINATION_BUCKET or not DYNAMO_TABLE:
    raise Exception('Please enter environment variables.')
  else:
    pass

def lambda_handler(event, context):
    # TODO implement
  try:
    if event:
      for single_event in event["Records"]:
        print('Single Event: {}' .format(str(single_event)))
        
        # checking if environment variables are given
        check_envs()

        # Reading bucket name and object name
        bucket_name = single_event['s3']['bucket']['name']
        file_key = single_event['s3']['object']['key']
            
        if not file_key.lower().endswith(('.mp4')):
          # logging.error('File is not mp4 ext')
          raise Exception('File is not of mp4 ext')

        
        download_path = '/tmp/{}{}'.format(uuid.uuid4(),  file_key.split("/")[-1])

        s3_resource.meta.client.download_file(bucket_name, file_key, download_path)

        video_processing(file_key.split("/")[-1], download_path, DESTINATION_BUCKET.strip())

        # s3.meta.client.download_file('mybucket', 'hello.txt', '/tmp/hello.txt')
  except ClientError as e:
    logging.error(str(e))
    raise Exception(str(e))
  except Exception as e:
    logging.error(str(e))
    raise Exception(str(e))
