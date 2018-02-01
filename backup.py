import sys

from s3 import BackupS3


def run_backup():
    folder_path = sys.argv[sys.argv.index("-l") + 1]
    remote_folder_path = sys.argv[sys.argv.index("-r") + 1]
    backup = BackupS3(folder_path, remote_folder_path)
    backup.upload()


if __name__ == '__main__':
    run_backup()
