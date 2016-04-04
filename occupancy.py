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


def build_size_dictionary(root):
    size_byte = 'byte'
    size_percentage = 'percent'
    dir_list = 'dirs'
    result = {}
    # os.walk loop
    for dirpath, dirnames, filenames in os.walk(root):
        folder_size_byte = 0
        local_file_list = []
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            file_size_byte = os.path.getsize(os.path.join(dirpath, filename))
            folder_size_byte += file_size_byte
            result[full_path] = {size_byte: file_size_byte}
            local_file_list.append(full_path)

        result[dirpath] = {size_byte: folder_size_byte,
                           dir_list: tuple([os.path.join(dirpath, dirname) for dirname in dirnames])}

        if folder_size_byte:
            for local_file in local_file_list:
                result[local_file][size_percentage] = float(result[local_file][size_byte]) / result[dirpath][size_byte] * 100

    return result


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
    folder_size = build_size_dictionary(os.curdir)
    pprint.pprint(folder_size)


if __name__ == '__main__':
    main()
