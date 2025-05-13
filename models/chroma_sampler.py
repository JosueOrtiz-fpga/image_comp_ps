import numpy as np

def chroma_subsample(pixel_group):
    """
    Subsamples a group of 4 x 2 YCbCr pixels using 4:2:0

    Parameters:
        pixel_group(np.ndarray) : a 4 x 2 matrix of YCbCr pixels
    Returns:
        subsample_group(tupple): a 4 x 2 matrix of subsampled YCbCr pixels
    """
    print(pixel_group.shape)
    block0 = np.concatenate((pixel_group[0][0:2], pixel_group[1][0:2]))
    block1 = np.concatenate((pixel_group[0][2:4], pixel_group[1][2:4]))
    print(pixel_group)
    print('\n')
    print(block0)
    print('\n')
    print(block1)

chroma_subsample(np.random.random_integers(50,255,(2,4,3)))
