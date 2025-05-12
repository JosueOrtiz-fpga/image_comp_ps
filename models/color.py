
def rgb_2_ycbcr(rgb):
    """
    Converts an RGB pixel to a the YCbCr color space

    Parameters:
        rgb(tupple) : a Red-Green-Blue pixel
    Returns:
        pixel(tupple): a YCbCr pixel
    """
    red, green, blue = rgb
    pixel = (red,green,blue)
    return pixel

print(rgb_2_ycbcr((10,11,12)))
print(type(rgb_2_ycbcr((10,11,12))))
