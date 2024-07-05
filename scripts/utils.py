import os 
import shutil

path_to_tmp = 'tmp'
path_to_lambdas = 'backend/lambda'

def destroy_tmp_folder():
    if os.path.exists(path_to_tmp):
        shutil.rmtree(path_to_tmp)

def init_tmp_folder():
    destroy_tmp_folder()
    os.mkdir(path_to_tmp)

def exit_helper():
    destroy_tmp_folder()
    exit()

def get_layer_name(lambda_name):
    return lambda_name + '_layer'
    


