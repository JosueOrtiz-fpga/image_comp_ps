import numpy as np
import matplotlib.pyplot as plt
import cv2

def dct2_mat(n):
    mat = np.zeros((n,n))
    for p in range(n):
        for q in range(n):
            if p ==0:
                mat[p,q] = 1/np.sqrt(n)
            else:
                mat[p,q] = np.sqrt(2/n) * np.cos((np.pi*(2*q+1)*p)/(2*n))
    return mat

def calc_2d_dct(input_matrix):
    dct2_t_mat = dct2_mat(8)
    dct2_t_mat_transpose = dct2_t_mat.T
    return dct2_t_mat @ input_matrix @ dct2_t_mat_transpose

def calc_2d_idct(input_matrix):
    dct2_t_mat = dct2_mat(8)
    dct2_t_mat_transpose = dct2_t_mat.T
    return dct2_t_mat_transpose @ input_matrix @ dct2_t_mat

def img_2_blocks(img, n):
    shape = img.shape
    if len(shape) == 3:
        height, width, depth = img.shape
    if len(shape) == 2:
        height,width = img.shape
    matrices = []
    for i in range(0, (height+1) - n, n):
        for j in range(0, (width+1) - n, n):
            matrix = img[i:i + n, j:j + n]
            matrices.append(matrix)
    return matrices

def blocks_2_img(blocks, height, width):
    # cocnatenating
    num_blocks_row = int((width + 1)/8)
    num_rows = int((height + 1)/8)
    img2_rows_of_blocks = []

    # concatenate blocks into rows
    for i in range(num_rows):
        img2_rows_of_blocks.append(np.concatenate(blocks[num_blocks_row*i:num_blocks_row*(i+1)],axis=1))

    #concatenate rows into matrix
    img2 = np.concatenate(img2_rows_of_blocks, axis=0)
    return img2

def dct_blocks(blocks):
    blocks_tf = []
    for block in blocks:
        blocks_tf.append(calc_2d_dct(block))
    return blocks_tf

def mask(n, coef_num, mat):
    # generate mask
    height, width, depth = mat.shape
    mask_matrix = np.zeros((height,width,depth),'unit8')
    for m in range(0,n):
        for n in range(0,n-m):
            mask_matrix[m,n] = (1,1,1)
    # apply mask
    return mat * mask_matrix

# image reading
img= cv2.imread("cameraman.tiff",cv2.IMREAD_GRAYSCALE)
height, width = img.shape

matrices = img_2_blocks(img, 8)
matrices2 = dct_blocks(dct_blocks(matrices))
print(matrices[0])
print(matrices2[0])

print('\n')
print(calc_2d_idct(calc_2d_dct(matrices[0])))
# img2 = blocks_2_img(matrices2,height, width)

# #display
# cv2.imshow("Image 1", img)
# cv2.imshow("Image 2", img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
