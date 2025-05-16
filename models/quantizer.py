import numpy as np

QY = np.array([
[16, 11, 10, 16, 24, 40, 51, 61],
[12, 12, 14, 19, 26, 58, 60, 55],
[14, 13, 16, 24, 40, 57, 69, 56],
[14, 17, 22, 29, 51, 87, 80, 62],
[18, 22, 37, 56, 68, 109, 103, 77],
[24, 35, 55, 64, 81, 104, 113, 92],
[49, 64, 78, 87, 103, 121, 120, 101],
[72, 92, 95, 98, 112, 100, 103, 99]
])

QC = np.array([
[17, 18, 24, 47, 99, 99, 99, 99],
[18, 21, 26, 66, 99, 99, 99, 99],
[24, 26, 56, 99, 99, 99, 99, 99],
[47, 66, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99]
])


def q_to_s(q):
    """
    Converts quality factor [1,100] to quant table scaling factor
    Formula is from Independent JPEG Group

    Parameters:
        q(int) : number in the range [1,100]
    Returns:
        s(int): quant table scaling factor
    """
    if q < 50:
        s = 5000/q
    else:
        s = 200 - 2*q

    return s/100

def quant_block(q, block, is_luma):
    """
    Quantizes an 8 x 8 block of DCT coefficients using the base
    JPEG quant tables for Y and Chroma and Quality factor

    Parameters:
        q(int) : Quality Factor in the range [1,100], 1 is highest compression
        block(np.ndarray): 8 x 8 matrix of DCT coefficients
        is_luma(boolean): True = matrix corresponds to Luma pixel data
    Returns:
        block_q(np.ndarray): quantized input block
    """
    if is_luma:
        qt = q_to_s(q) * QY + 0.5
    else:
        qt = q_to_s(q) * QC + 0.5
    
    return np.floor(block/qt)


test_matrix = np.random.random_integers(-20,20,(8,8))
print(test_matrix)
print("----------")
print(quant_block(90,test_matrix,False))

