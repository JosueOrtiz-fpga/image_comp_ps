import numpy as np
import cv2

def dct2_mat(n):
    mat = np.zeros((n,n),)
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
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
