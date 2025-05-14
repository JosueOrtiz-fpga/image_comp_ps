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
            y.append(np.uint8(pixel[0]))
            cb.append(np.uint8(pixel[1]))
            cr.append(np.uint8(pixel[2]))
        y_row.append(y)
        
        # cb_row.append(np.ndarray(cb))
        # cr_row.append(np.ndarray(cr))
    # print("-------------")
    height, width, depth = mat.shape
    y_mat = np.zeros((height, width),mat.dtype)
    for m in range(len(y_row)):
        y_mat[m] = y_row[m]
    print(mat)
    print("-------------")
    print(y_mat)
    # y_mat = np.concatenate(y_row, axis=1)
    # print(y_mat)
    # cb_mat = np.concatenate(cb_row, axis=0)
    # cr_mat = np.concatenate(cr_row, axis=0)
    # print(mat)
    # print("-------------")
    # print(y_mat)
        


chroma_subsample_mat(np.random.random_integers(50,255,(3,4,3)))
