import numpy as np

def chroma_subsample_mat(mat):
    """
    Subsamples a matrix of YCbCr pixels using 4:2:0

    Parameters:
        mat(np.ndarray) : an n x n matrix of YCbCr pixels
    Returns:
        subsample_mat(np.ndarray): a subsampled YCbCr matrix
    """
    y_row = []
    cb_row = []
    cr_row = []
    for row in mat:
        y = []
        cb = []
        cr=[]
        for pixel in row:
            y.append(pixel[0])
            cb.append(pixel[1])
            cr.append(pixel[2])
        y_row.append(y)
        cb_row.append(cb)
        cr_row.append(cr)
    print(mat)
    print("----------------")
    print(y_row)
    print(cb_row)
    print(cr_row)
        
        


chroma_subsample_mat(np.random.random_integers(50,255,(2,4,3)))
