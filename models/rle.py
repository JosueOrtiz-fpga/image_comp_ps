import numpy as np
import cv2


def rle(input_list):
    """
    Does run length encoding on input 1-D array

    Parameters:
        input_list(list) : 1-D array or list
    Returns:
        rle_code(list): run-length-encoded list: sizeCharacter, sizeCharacter, ...
    """
    rle_code = []
    temp_char = input_list[0]
    count = 1
    for char in input_list[1:]:
        if char == temp_char:
            count += 1
        else:
            rle_code.append(count)
            rle_code.append(temp_char)
            count = 1
            temp_char = char
    # append the last code before exiting loop
    rle_code.append(count)
    rle_code.append(temp_char)
    # remove trailing zero compnents
    if rle_code[-1] == 0:
        rle_code = rle_code[:-2]
    return rle_code
    
