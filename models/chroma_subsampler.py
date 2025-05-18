import numpy as np

def block_subsample(block):
    """
    Applies a 4:2:0 subsample to a 2 x 4 block of Y, Cb, or Cr components

    Parameters:
        block(np.ndarray) : a 2 x 4 matrix of Y, Cb, or Cr components
    Returns:
        subsample_block(np.ndarray): a subsampled 2 x 4 Y, Cb, or Cr block
    """
    samples = [block[0,0],block[0,2]]
    subsample_block = np.zeros((2,4), dtype=np.uint8)
    for i in range(2):
        for j in range(4):
            subsample_block[i,j] = samples[int(j/2)]
    return subsample_block

def block_subsample_avg(block):
    """
    Applies a 4:2:0 subsample to a 2 x 4 block of Y, Cb, or Cr components
    by averaging the samples

    Parameters:
        block(np.ndarray) : a 2 x 4 matrix of Y, Cb, or Cr components
    Returns:
        subsample_block(np.ndarray): a subsampled 2 x 4 Y, Cb, or Cr block
    """
    samples = []
    for i in range(0,4,2):
        samples.append(np.uint8(np.mean(block[0:2, i:i+2])))
    subsample_block = np.zeros((2,4), dtype=np.uint8)
    for i in range(2):
        for j in range(4):
            subsample_block[i,j] = samples[int(j/2)]
    return subsample_block

def mat_subsample(mat):
    """
    Applies a 4:2:0 subsample to an n x n matrrix of Y, Cb, or Cr components

    Parameters:
        mat(np.ndarray) : an n x n matrix of Y, Cb, or Cr components
    Returns:
        subsample_mat(np.ndarray): a subsampled n x n Y, Cb, or Cr matrix
    """
    block_h = 2
    block_w = 4
    height, width = mat.shape
    subsample_mat = np.zeros((height,width),mat.dtype)
    for m in range(0,height,block_h):
        for n in range(0,width,block_w):
            block = mat[m:m+block_h, n:n+block_w]
            subsample_mat[m:m+block_h,n:n+block_w] = block_subsample(block)
    return subsample_mat

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

def pad_dims(shape):
    """
    Adjusts the dimensions of an image to be a multiple of 8 x 8 blocks

    Parameters:
        shape(tupple) : a (height,width) tupple
    Returns:
        adj_shape(tupple): an adjusted (height,width) tupple
    """
    adj_shape = []
    for i in range(2):
        if(shape[i] % 8 == 0): adj_shape.append(shape[i])
        else: adj_shape.append(shape[i] + (8-shape[i]%8))
    return tuple(adj_shape)
