import numpy as np

def matrices_equal(exp, result):
    """ Check if matrices are equal"""
    if(exp.shape != result.shape):
        raise Exception("Input matrices are not the same size")
    for exp_row, result_row in zip(exp,result):
            for e_n, r_n in zip(exp_row, result_row):
                assert(e_n == r_n)

"""
Color Tests
"""
import color
def test_pixel_color_conv():
    """ Pixel Color Conversion Test"""
    test_pixels = [(0,0,0),(50, 100, 125),(255 , 255, 255)]
    for pixel in test_pixels:
        result = color.ycbcr_2_rgb(color.rgb_2_ycbcr(pixel))
        assert(result == pixel)
    print("pixel_color_conversion PASS")

def test_img_color_conv():
    """ Image Color Conversion Test"""
    test_img = np.random.randint(0,255,(256,256,3))
    result = color.ycbcr_mat_2_rgb(color.rgb_mat_2_ycbcr(test_img))

    # checkign each element in the arrays
    for t_row,r_row in zip(test_img,result):
        for t_pixel, r_pixel in zip(t_row, r_row):
            for t, r in zip(t_pixel,r_pixel):
                # due to imprecision in conversion, values can be off by 1
                assert(abs(t-r) <= 1)
    print("image_color_conversion PASS")



"""
Subsampler Tests
"""
import chroma_subsampler as cs
def test_block_sub_sample():
    """
    Block SubSample Test
    """
    num_bloks = 3
    test_blocks  = []
    for i in range(num_bloks):
        test_blocks.append(np.random.randint(0,255,(2,4)))
    
    results = []
    for block in test_blocks:
        results.append(cs.block_subsample(block))
    
    for block in test_blocks:
        block[:,0:2].fill(block[0,0])
        block[:,2:4].fill(block[0,2])

    # checkign each element in the arrays
    for test_block, result_block in zip(test_blocks, results):
        matrices_equal(test_block, result_block)
    print("block_sub_sample PASS")    

def test_block_sub_sample_avg():
    """
    Block SubSample Test
    """
    num_bloks = 3
    test_blocks  = []
    for i in range(num_bloks):
        test_blocks.append(np.random.randint(0,255,(2,4)))
    
    results = []
    for block in test_blocks:
        results.append(cs.block_subsample_avg(block))
    
    for block in test_blocks:
        block[:,0:2].fill(np.mean(block[:,0:2]))
        block[:,2:4].fill(np.mean(block[:,2:4]))
    
    # checkign each element in the arrays
    for test_block, result_block in zip(test_blocks, results):
        matrices_equal(test_block, result_block)
    print("block_sub_sample_avg PASS")   

def test_mat_subsample():
    test_mat = np.random.randint(0,255,(4,4))
    result = cs.mat_subsample(test_mat)

    height, width = test_mat.shape
    for m in range(0,height,2):
        for n in range(0,width,2):
            test_mat[m:m+2,n:n+2].fill(test_mat[m,n])
    
    matrices_equal(test_mat, result)
    print("mat_subsample PASS")   

test_pixel_color_conv()
test_img_color_conv()
test_block_sub_sample()
test_block_sub_sample_avg()
test_mat_subsample()
