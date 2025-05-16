import numpy as np
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
    for t_row,r_row in zip(test_img,result):
        for t_pixel, r_pixel in zip(t_row, r_row):
            for t, r in zip(t_pixel,r_pixel):
                # due to imprecision in conversion, values can be off by 1
                assert(abs(t-r) <= 1)
    
    print("image_color_conversion PASS")

test_pixel_color_conv()
test_img_color_conv()


