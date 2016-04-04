"""
To calculate how much bytes each folders use
"""
# TODO : os.walk loop
# TODO : folder size :
#           monkut, Calculating a directory size using Python?, Sep 8 '09,
#           http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
# TODO : Consider applying scandir for Python 3.x
#           monkut, Calculating a directory size using Python?, Jan 29 '09,
#           http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
# TODO : Recursive summation?
# TODO : Data presentation in GUI?
# TODO : Data presentation : in Bytes & in percentage


import os
import pprint


def sub_folder_size(sub_folder):
    """
    :param sub_folder: path to a sub folder
    :return: size of all the files
    """
    total_size = 0

    # os.walk loop
    for dirpath, dirnames, filenames in os.walk(sub_folder):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            file_size_byte = os.path.getsize(os.path.join(dirpath, filename))
            total_size += file_size_byte

    return total_size


def normalize(size_sequence):
    """
    :param size_sequence: list or tuple of [k1, k2, ... , kn]
    :return: a tuple of (k1/(k1 + k2 + ... + kn), k2/(k1 + k2 + ... + kn), ... , kn/(k1 + k2 + ... + kn),)
    """
    total = sum(size_sequence)
    denominator = 1.0 / total
    result = [item * denominator for item in size_sequence]
    return tuple(result)


def main():
    folder_size = sub_folder_size(os.curdir)
    pprint.pprint(folder_size)


if __name__ == '__main__':
    main()
