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

img = cv2.imread("cameraman.tiff")
block0 = np.zeros((8,8,3), img.dtype)
for m in range(8):
    for n in range(8):
        block0[m,n] = img[m,n]

height, width, depth = img.shape
matrices = []
# range stop index is exclusive: + 1 needed
for i in range(0, (height+1) - 8, 8):
    for j in range(0, (width+1) - 8, 8):
        matrix = img[i:i + 8, j:j + 8]
        matrices.append(matrix)

print(matrices[0])
print(block0 == matrices[0])


