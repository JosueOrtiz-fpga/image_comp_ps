import numpy as np
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
    dct2_t_mat_transpose = dct2_mat(8).T
    return np.dot(dct2_t_mat_transpose, np.dot(dct2_t_mat, input_matrix))

# image reading
img = cv2.imread("cameraman.tiff")
height, width, depth = img.shape

# image division into 8x8 blocks
matrices = []
for i in range(0, (height+1) - 8, 8):
    for j in range(0, (width+1) - 8, 8):
        matrix = img[i:i + 8, j:j + 8]
        matrices.append(matrix)

# dct of all 8x8 blocks
dct_blocks = []
for block in matrices:
    dct_blocks.append(calc_2d_dct(block))

# masking
mask_matrix = np.zeros((8,8,3),img.dtype)
for m in range(0,4):
    for n in range(0,4-m):
        mask_matrix[m,n] = (1,1,1)

dct_blocks_masked = []
for block in dct_blocks:
    dct_blocks_masked.append(block * mask_matrix)

# inverse dct
img2_blocks = []
for block in dct_blocks_masked:
    img2_blocks.append(calc_2d_dct(block))
# cocnatenating
num_blocks_row = int((width + 1)/8)
num_rows = int((height + 1)/8)
img2_rows_of_blocks = []

# concatenate blocks into rows
for i in range(num_rows):
    img2_rows_of_blocks.append(np.concatenate(img2_blocks[0:num_blocks_row],axis=1))

#concatenate rows into matrix
img2 = np.concatenate(img2_rows_of_blocks, axis=0)
print(img2.shape)

# display
cv2.imshow("Image", img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
