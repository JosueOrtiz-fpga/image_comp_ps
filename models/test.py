import numpy as np


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
        for t_row, r_row in zip(test_block,result_block):
            for t_n, r_n in zip(t_row, r_row):
                assert(t_n == r_n)
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
        for t_row, r_row in zip(test_block,result_block):
            for t_n, r_n in zip(t_row, r_row):
                assert(t_n == r_n)
    print("block_sub_sample_avg PASS")   

test_pixel_color_conv()
test_img_color_conv()
test_block_sub_sample()
test_block_sub_sample_avg()
