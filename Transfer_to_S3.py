import boto3, os, shutil

s3 = boto3.resource('s3')

bucket = s3.Bucket('netball-ml-processing')

print(bucket.objects)

source_path = '../'
destination_path = 'processed'
file = '99-20180621221607-00.jpg'

#s3.meta.client.upload_file('/Users/andrewhammond/s3_upload.jpg','netball-ml-processing', 's3_upload.jpg')

s3.meta.client.upload_file(source_path + file,'netball-ml-processing', file)

#once pushed to s3 need to shift locally.
shutil.move(source_path + file, source_path + destination_path)


