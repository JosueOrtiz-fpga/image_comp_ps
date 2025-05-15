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

def block_subsample(block):
    """
    Applies a 4:2:0 subsample to a 2 x 4 block of Y, Cb, or Cr components

    Parameters:
        block(np.ndarray) : a 2 x 4 matrix of Y, Cb, or Cr components
    Returns:
        subsample_block(np.ndarray): a subsampled 2 x 4 Y, Cb, or Cr block
    """
    samples = [block[0][0],block[0][2]]
    subsample_block = np.zeros((2,4), dtype=np.uint8)
    for i in range(2):
        for j in range(4):
            print(samples[int(j/2)])
            subsample_block[i,j] = samples[int(j/2)]
    return block_subsample

def chroma_subsample_mat(mat):
    """
    Subsamples a matrix of YCbCr pixels using 4:2:0

    Parameters:
        mat(np.ndarray) : an n x n matrix of YCbCr pixels
    Returns:
        subsample_mat(np.ndarray): a subsampled YCbCr matrix
    """
    y_vec, cb_vec, cr_vec = separate_pixel_comps(mat)

    shape= (mat.shape[0], mat.shape[1])
    y_mat, cb_mat, cr_mat = (vec_2_mat(shape,y_vec), vec_2_mat(shape,cb_vec), vec_2_mat(shape,cr_vec))



        
    return y_mat, cb_mat, cr_mat

test_matrix = np.random.random_integers(50,255,(2,4))
print(test_matrix)
print("-------------------")
print(block_subsample(test_matrix))
