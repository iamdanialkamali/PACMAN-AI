import zipfile
import os
import sys

if __name__ == '__main__':
    cwd = os.getcwd()
    file_name = "asg01_%s.zip" % sys.argv[1]
    zip_file = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
    zip_file.write('searchFunctions.py')
    zip_file.write('searchProblems.py')
    zip_file.close()
