import boto3

s3 = boto3.resource('s3')

bucket = s3.Bucket('netball-ml-processing')

print(bucket.objects)

s3.meta.client.upload_file('/Users/andrewhammond/s3_upload.jpg','netball-ml-processing', 's3_upload.jpg')

#so simple

