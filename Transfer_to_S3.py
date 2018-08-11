import boto3, os, shutil

session = boto3.Session(profile_name='default')

s3 = boto3.resource('s3')

bucket = s3.Bucket('netball-ml-processing')

#print(bucket.objects)

#needs to be run with *** sudo ****  otherwise it won't work...

#change to the motion working Directory

os.chdir('/home/motion/netball-images')

print (str(os.getcwd()))

for f in os.listdir(os.getcwd()):
    print("looping in file")

    file_name, file_ext = os.path.splitext(f)

    #need to check the file starts with 2 (as in the timestamp) and is a .jpg
    if file_ext == '.jpg':
        print("working with this file " + f)

        # s3.meta.client.upload_file('/Users/andrewhammond/s3_upload.jpg','netball-ml-processing', 's3_upload.jpg')
        s3.meta.client.upload_file(f, 'netball-ml-processing', f)

        print ("should of uploaded to s3")

        # once pushed to s3 need to shift locally.
        shutil.move(f, '/home/motion/netball-images/shifted_to_s3')

        print ("should of moved the file locally")







