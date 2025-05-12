import numpy as np
import cv2

def dct2_mat(n):
    """
    Returns an n x n DCT tranform matrix

    Parameters:
        n(int): matrix dimension desired
    Returns:
        mat(numpy.ndarray): An n x n DCT transform matrix 
    """
    mat = np.zeros((n,n))
    for p in range(n):
        for q in range(n):
            if p ==0:
                mat[p,q] = 1/np.sqrt(n)
            else:
                mat[p,q] = np.sqrt(2/n) * np.cos((np.pi*(2*q+1)*p)/(2*n))
    return mat

def calc_2d_dct(matrix):
    """
    Returns the 2-D DCT of the input matrix

    Parameters:
        matrix(numpy.ndarray): matrix, n x n
    Returns:
        dct2(numpy.ndarray): 2D DCT transform of the input matrix 
    """
    dct2_t_mat = dct2_mat(matrix.shape[0])
    dct2_t_mat_transpose = dct2_t_mat.T
    return dct2_t_mat @ matrix @ dct2_t_mat_transpose

def calc_2d_idct(matrix):
    """
    Returns the 2-D Inverse DCT of the input matrix

    Parameters:
        matrix(numpy.ndarray): matrix of 2-D DCT coefficients, n x n
    Returns:
        idct2(numpy.ndarray): Inverse DCT, n x n matrix
    """
    dct2_t_mat = dct2_mat(matrix.shape[0])
    dct2_t_mat_transpose = dct2_t_mat.T
    return dct2_t_mat_transpose @ matrix @ dct2_t_mat

def img_2_blocks(img, n):
    """
    Breaks the input image into n x n blocks

    Parameters:
        img(numpy.ndarray): matrix representing an image
        n(int)            : block size to be used
    Returns:
        matrices(list): list of n x n blocks
    """
    matrices = []
    for i in range(0, (img.shape[0]+1) - n, n):
        for j in range(0, (img.shape[1]+1) - n, n):
            matrix = img[i:i + n, j:j + n]
            matrices.append(matrix)
    return matrices

def blocks_2_img(blocks, height, width):
    """
    Concatenates input blocks into an image (matrix)

    Parameters:
        blocks(list) : list of n x n blocks to concatenate
        height(int)  : expected height of return image
        width(int)   : expected width of return image
    Returns:
        img(np.ndarray): matrix of concatenated blocks
    """

    n = blocks[0].shape[0]
    blocks_p_row = int((width + 1)/n)
    num_rows = int((height + 1)/n)

    rows = []
    for i in range(num_rows):
        rows.append(np.concatenate(blocks[blocks_p_row*i:blocks_p_row*(i+1)],axis=1))

    img = np.concatenate(rows, axis=0)
    return img

def dct_blocks(blocks):
    """
    Applies the 2D DCT to a list of blocks

    Parameters:
        blocks(list) : list of n x n blocks
    Returns:
        blocks_tf(list): list of n x n transformed blocks
    """
    blocks_tf = []
    for block in blocks:
        blocks_tf.append(calc_2d_dct(block))
    return blocks_tf

def idct_blocks(blocks):
    """
    Applies the 2D Inverse DCT to a list of blocks

    Parameters:
        blocks(list) : list of n x n blocks with DCT corefficients
    Returns:
        blocks_tf(list): list of n x n transformed blocks
    """
    blocks_tf = []
    for block in blocks:
        blocks_tf.append(calc_2d_idct(block))
    return blocks_tf

def int_blocks(blocks):
    """
    Converts input blocks' members to np.unit8 type

    Parameters:
        blocks(list) : list of n x n blocks with DCT corefficients
    Returns:
        blocks_int(list): list of n x n transformed blocks
    """
    blocks_int = []
    for block in blocks:
        blocks_int.append(block.astype(np.uint8))
    return blocks_int

# def mask(n, coef_num, mat):
#     # generate mask
#     height, width, depth = mat.shape
#     mask_matrix = np.zeros((height,width,depth),'unit8')
#     for m in range(0,n):
#         for n in range(0,n-m):
#             mask_matrix[m,n] = (1,1,1)
#     # apply mask
#     return mat * mask_matrix

# image reading
src_img= cv2.imread("cameraman.tiff",cv2.IMREAD_GRAYSCALE)
blocks = int_blocks(idct_blocks(dct_blocks(img_2_blocks(src_img, 8))))

height, width = src_img.shape
result_img = blocks_2_img(blocks,height, width)

#display
cv2.imshow("Image 1", src_img)
cv2.imshow("Image 2", result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
