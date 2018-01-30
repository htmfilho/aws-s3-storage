import os
import boto3
import botocore


class BackupS3:
  s3 = None
  bucket = None
  folder_path = None
  remote_folder_path = None
  files_to_upload = []
  files_uploaded = []

  def __init__(self, folder_path, remote_folder_path):
    self.s3 = boto3.resource('s3')
    self.bucket = self.s3.Bucket('hildeberto')
    self.folder_path = folder_path
    self.remote_folder_path = remote_folder_path

  def upload_file(self, file_path):
    total_uploaded = len(self.files_uploaded)
    total_to_upload = len(self.files_to_upload)
    percent = (total_uploaded / total_to_upload) * 100
    relative_path = get_relative_path(self.folder_path, file_path)
    key = "{}{}".format(self.remote_folder_path, relative_path)
    print('Uploading {:d} of {:d} {} -> {} {:04.2f}%'.format(total_uploaded + 1, 
                                                       total_to_upload, 
                                                       file_path,
                                                       key, 
                                                       percent))
    self.bucket.upload_file(file_path, key)
    self.files_uploaded.append(file_path)
    print("Done! 100%")

  def download_file(self, remote_file_path):
    try:
      relative_path = get_relative_path(self.remote_folder_path, 
                                        remote_file_path)
      self.bucket.download_file(remote_file_path, 
                                '{}{}'.format(self.folder_path, relative_path))
    except botocore.exceptions.ClientError as e:
      if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
      else:
        raise

  def upload_files(self):
    for file_path in self.files_to_upload:
      self.upload_file(file_path)

  def download_files(self):
    for obj in self.bucket.objects.filter(Prefix=self.remote_folder_path):
      self.download_file(obj.key)

  def explore_local_folder(self):
    print('Exploring folder {}'.format(self.folder_path))
    for path, dirs, files in os.walk(self.folder_path):
      for f in files:
        file_path = '{}/{}'.format(path, f)
        file_path = file_path.replace("//", "/")
        self.files_to_upload.append(file_path)

  def upload(self):
    self.explore_local_folder()
    self.upload_files()

  def download(self):
    self.download_files()


def get_relative_path(base_path, file_path):
  return file_path.replace(base_path, "")
