import numpy as np

def rgb_2_ycbcr(rgb):
    """
    Converts an RGB pixel to a the YCbCr color space

    Parameters:
        rgb(tupple) : a Red-Green-Blue pixel
    Returns:
        pixel(tupple): a YCbCr pixel
    """
    red, green, blue = rgb
    y= round(0 + (0.299*red) + (0.587 * green) + (0.114 * blue))
    cb = round(128 - (0.168736 * red) - (0.331264 * green) + (0.5 * blue))
    cr = round(128 + (0.5 * red) - (0.418688 * green) - (0.081312 * blue))
    ycbcr = (y,cb,cr)
    return ycbcr

def ycbcr_2_rgb(ycbcr):
    """
    Converts an YCbCr pixel to a the RGB color space

    Parameters:
        ycbcr(tupple) : a Y-Cb-Cr pixel
    Returns:
        pixel(tupple): a RGB pixel
    """
    y,cb,cr = ycbcr
    r = round(y + 1.402*(cr-128))
    g = round(y - 0.344136*(cb-128) - 0.714136*(cr-128))
    b = round(y + 1.772*(cb-128))
    rgb = (r,g,b)
    return rgb

def rgb_mat_2_ycbcr(mat):
    """
    Converts a matrix of RGB pixels to the YCbCr color space

    Parameters:
        mat(ndarray) : a matrix of RGB pixels
    Returns:
        ycbcr_mat(ndarray): a matrix of YCbCr pixels
    """
    height, width, depth = mat.shape
    ycbcr_mat = np.zeros((height, width, depth), dtype=mat.dtype)
    for m in range(height):
        for n in range(width):
            ycbcr_mat[m][n] = np.uint8(rgb_2_ycbcr(mat[m][n]))
    return ycbcr_mat

def ycbcr_mat_2_rgb(mat):
    """
    Converts a matrix of YCbCr pixels to the RGB color space

    Parameters:
        mat(ndarray) : a matrix of YCbCr pixels
    Returns:
        rgb_mat(ndarray): a matrix of RGB pixels
    """
    height, width, depth = mat.shape
    rgb_mat = np.zeros(mat.shape, dtype=mat.dtype)
    for m in range(height):
        for n in range(width):
            rgb_mat[m][n] = ycbcr_2_rgb(mat[m][n])
    return rgb_mat


