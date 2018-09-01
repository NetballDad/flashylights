import boto3, os, shutil

session = boto3.Session(profile_name='default')

s3 = boto3.resource('s3')

bucket = s3.Bucket('netball-ml-processing')

#print(bucket.objects)

#needs to be run with *** sudo ****  otherwise it won't work...

while True:

    #change to the motion working Directory
    os.chdir('/home/motion/netball-images')

    print (str(os.getcwd()))

    for f in os.listdir(os.getcwd()):
        print("looping in file")

        file_name, file_ext = os.path.splitext(f)

        #need to check the file starts with 2 (as in the timestamp) and is a .jpg
        if file_ext == '.jpg':
            print("working with this file " + f)

            print("about to upload " + str(datetime.datetime.now()) + "\r\n")
            # s3.meta.client.upload_file('/Users/andrewhammond/s3_upload.jpg','netball-ml-processing', 's3_upload.jpg')
            s3.meta.client.upload_file(f, 'netball-ml-processing', f)

            print ("Uploaded to S3 " + str(datetime.datetime.now()) + "\r\n")

            # once pushed to s3 need to shift locally.
            shutil.move(f, '/home/motion/netball-images/shifted_to_s3')

            print ("should of moved the file locally")
    time.sleep(2)






