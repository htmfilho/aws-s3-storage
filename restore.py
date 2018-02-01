import sys

from s3 import BackupS3


def run_restore():
    folder_path = sys.argv[sys.argv.index("-l") + 1]
    remote_folder_path = sys.argv[sys.argv.index("-r") + 1]
    restore = BackupS3(folder_path, remote_folder_path)
    restore.download()


if __name__ == '__main__':
    run_restore()
