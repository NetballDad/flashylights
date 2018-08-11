import boto3, os, shutil

s3 = boto3.resource('s3')

bucket = s3.Bucket('netball-ml-processing')

print(bucket.objects)

#needs to be run with *** sudo ****  otherwise it won't work...

#change to the motion working Directory

os.chdir('/home/motion/netball-images')

for f in os.listdir(os.getcwd()):
    #print("into for files_processed")

    file_name, file_ext = os.path.splitext(f)

    #need to check the file starts with 2 (as in the timestamp) and is a .jpg
    if file_ext == '.jpg' and file_name[0:1] == '2':
        #print("into if statement")

        # s3.meta.client.upload_file('/Users/andrewhammond/s3_upload.jpg','netball-ml-processing', 's3_upload.jpg')
        s3.meta.client.upload_file(f, 'netball-ml-processing', f)

        # once pushed to s3 need to shift locally.
        shutil.move(f, '/home/motion/netball-images/shifted_to_s3')









