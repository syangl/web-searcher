import os


def del_files(dir_path):
    if os.path.isfile(dir_path):
        try:
            os.remove(dir_path)
        except BaseException as e:
            print(e)
    elif os.path.isdir(dir_path):
        file_list = os.listdir(dir_path)
        for file_name in file_list:
            tf = os.path.join(dir_path, file_name)
            del_files(tf)

