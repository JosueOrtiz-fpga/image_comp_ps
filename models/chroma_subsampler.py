import numpy as np

def separate_pixel_comps(mat):
    """
    Separate pixels in a matrix into their different components

    Parameters:
        mat(np.ndarray) : an n x n matrix of pixels with depth of 3
    Returns:
        pixels(tupple): a tupple with 3 list components containing pixel components
    """
    height, width, depth = mat.shape
    y_vec = []
    cb_vec = []
    cr_vec = []
    for row in mat:
        for pixel in row:
            y, cb, cr = pixel
            y_vec.append(y)
            cb_vec.append(cb)
            cr_vec.append(cr)
    return (y_vec, cb_vec, cr_vec)

def vec_2_mat(shape, vec):
    """
    Returns a matrix comprised of components in input vector

    Parameters:
        shape(tupple) : (height (num of rows), width (num of cols))
        vec(array)    : 1-D array of components
    Returns:
        mat(nd.array): matrix
    """
    mat = np.zeros(shape)
    height, width = shape
    for i in range(height):
        mat[i] = vec[width*i: width*(i+1)]
    return mat

def chroma_subsample_mat(mat):
    """
    Subsamples a matrix of YCbCr pixels using 4:2:0

    Parameters:
        mat(np.ndarray) : an n x n matrix of YCbCr pixels
    Returns:
        subsample_mat(np.ndarray): a subsampled YCbCr matrix
    """
    height, width, depth = mat.shape
    shape = (height,width)
    y_vec, cb_vec, cr_vec = separate_pixel_comps(mat)

        
    return (vec_2_mat(shape,y_vec), vec_2_mat(shape,cb_vec), vec_2_mat(shape,cr_vec))

test_matrix = np.random.random_integers(50,255,(4,4,3))
print(test_matrix)
print("-------------------")
print(chroma_subsample_mat(test_matrix))
