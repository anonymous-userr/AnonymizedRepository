#Load libraries.io zipped file - version 2020-01-12
import tarfile

file_path = 'path to dataset/libraries-1.6.0-2020-01-12.tar.gz'

with tarfile.open(file_path, 'r:gz') as tar:
    file_names = tar.getnames()
    print("Files in the folder:", file_names)

