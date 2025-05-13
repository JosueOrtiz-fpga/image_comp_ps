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
    y= 0 + (0.299*red) + (0.587 * green) + (0.114 * blue)
    cb = 128 - (0.168736 * red) - (0.331264 * green) + (0.5 * blue)
    cr = 128 + (0.5 * red) - (0.418688 * green) - (0.081312 * blue)
    return (y,cb,cr)

def ycbcr_2_rgb(ycbcr):
    """
    Converts an YCbCr pixel to a the RGB color space

    Parameters:
        ycbcr(tupple) : a Y-Cb-Cr pixel
    Returns:
        pixel(tupple): a RGB pixel
    """
    y,cb,cr = ycbcr
    r = y + 1.402*(cr-128)
    g = y - 0.344136*(cb-128) - 0.714136*(cr-128)
    b = y + 1.772*(cb-128)
    return (r,g,b)

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
    rgb_mat = np.zeros((height, width, depth), dtype=mat.dtype)
    for m in range(height):
        for n in range(width):
            rgb_mat[m][n] = np.uint8(ycbcr_2_rgb(mat[m][n]))
    return rgb_mat

test_mat = np.random.random_integers(50,255,(1,8,3))
print(test_mat)
print(rgb_mat_2_ycbcr(test_mat))
print(ycbcr_mat_2_rgb(rgb_mat_2_ycbcr(test_mat)))


