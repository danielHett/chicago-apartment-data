# used to deploy lambda code to aws. 
# the most recent layer is attatched to the lambda. 
import argparse
import os
import boto3
import botocore
import shutil
import utils
import subprocess

# a constant to tell us where all of the lambda code is stored. 
lambda_folder_path = 'backend/lambda/'

# set up the arguement parser. 
parser = argparse.ArgumentParser(description='deploy code to aws lambda')
parser.add_argument('name')

# create a client to communicate with s3. 
client = boto3.client('lambda')

# get the name of the lambda
lambda_name = parser.parse_args().name
path = lambda_folder_path + lambda_name

# does a folder exist for that lambda?
if not os.path.exists(path): 
    print('the lambda function could not be located. the path "' + path + '" does not exist.')
    utils.exit_helper()

# are all required files present?
required_files = ['handler.py', 'requirements.txt']
for required_file in required_files:
    file_name = lambda_folder_path + lambda_name + '/' + required_file
    if not os.path.isfile(file_name):
        print('the file "' + file_name + '" is missing. add it before running this script.')
        utils.exit_helper()

# create a clean tmp folder to put things. 
utils.init_tmp_folder()

# Copy all files into the temporary directory. 
shutil.copytree(path, utils.path_to_tmp + '/package')

subprocess.run(['pip3', 'install', '-r', utils.path_to_tmp + '/package/requirements.txt', '--target', utils.path_to_tmp + '/package']) 

# create the zip file. 
shutil.make_archive(utils.path_to_tmp + '/deployment_file', 'zip', utils.path_to_tmp + '/package')

# does the function exist
try:
    response = client.get_function(
        FunctionName='parse_pages',
    )
except client.exceptions.ResourceNotFoundException:
    print('the lambda has not been created in aws')
    utils.exit_helper()

except: 
    print('there was an error communcating with aws')
    utils.exit_helper()

# okay it does, update the code
with open(utils.path_to_tmp + '/deployment_file.zip', 'rb') as f:
    package_bytes = f.read()

try:
    response = client.update_function_code(
        FunctionName=lambda_name,
        ZipFile=package_bytes,
        Publish=False,
        Architectures=['x86_64']
    )
except Exception as e:
    print('there was an error while updating the code')
    print(e)
    utils.exit_helper()

utils.exit_helper()