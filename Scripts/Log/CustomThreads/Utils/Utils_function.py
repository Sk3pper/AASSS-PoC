import os


# scrive i dati in un file
# se presente gli appende
# se non presente crea il file da zero
import socket


def write_data(path_file_name, data):
    """
    :type path_file_name: str
    :type data: str
    """
    # file does not exist
    if not os.path.isfile(path_file_name):
        with open(path_file_name, "w+") as f:
            f.write("timestamp\tPhase\tFrom\tTo\tPayload\n")
            f.write(data)
            print "     " + str(data[:-2]) + " are saved in path:" + path_file_name
            return True
    # file exists
    else:
        with open(path_file_name, "a") as f:
            f.write(data)
            print "     " + str(data[:-2]) + " are saved in path:" + path_file_name
            return True


# check if exists a user dir -> if not create it
def check_dir(path_user):
    if not os.path.isdir(path_user):
        os.makedirs(path_user)
