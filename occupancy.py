"""
To calculate how much bytes each folders use
"""
# TODO : Consider applying scandir for Python 3.x
#           monkut, Calculating a directory size using Python?, Jan 29 '09,
#               http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
#           16.1. os — Miscellaneous operating system interfaces, Feb 27 '16,
#               https://docs.python.org/3.5/library/os.html#os.scandir
# TODO : Data presentation in GUI?


import os
import pprint
import sys
import time


def folder_fraction(path):
    """
    :param path:
    :return: tuple of (path, size in Byte, size in fraction 0~1)
    """
    time_start = time.clock()

    abs_path = os.path.abspath(path)

    name_list = []
    size_list = []
    for name in os.listdir(abs_path):
        full_path = os.path.join(abs_path, name)
        name_list.append(full_path)

        size = 0
        if os.path.isfile(full_path):
#           monkut, Calculating a directory size using Python?, Sep 8 '09,
#               http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
            size = os.path.getsize(full_path)
        elif os.path.isdir(full_path):
            size = sub_folder_size(full_path)
        size_list.append(size)

    normalized_size_list = normalize(size_list)
    result = list(zip(name_list, size_list, normalized_size_list))
    # Andrew Dalke and Raymond Hettinger, Sorting HOW TO, https://docs.python.org/3/howto/sorting.html#key-functions
    result.sort(key=lambda item: -item[1])

    time_end = time.clock()
    print("elapsed time = %6.4g (sec)" % (time_end - time_start))
    return tuple(result)


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
            if os.path.exists(full_path):
#           monkut, Calculating a directory size using Python?, Sep 8 '09,
#               http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
                file_size_byte = os.path.getsize(full_path)
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


def main(path=os.curdir):
    fraction = folder_fraction(path)
    pprint.pprint(fraction)

    names, sizes, fractions = zip(*fraction)

    folder_size = sub_folder_size(path)
    print(folder_size)
    print("error = %d" % (folder_size - sum(sizes)))


if __name__ == '__main__':
    main(sys.argv[1])
