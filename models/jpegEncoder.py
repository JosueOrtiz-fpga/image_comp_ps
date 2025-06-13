"""
JPEG Baseline Encoder - Complete Template
Based on ITU-T.81 Standard

This template shows the high-level structure of our JPEG encoder implementation.
We'll build each component step by step.
"""

import numpy as np
from coreEncoder import CoreEncoder,t_comp
import string
import cv2

#---------------
# JPEG Encoder

class JPEGEncoder:
    """
    Main JPEG Baseline Encoder Class
    
    This class orchestrates the entire JPEG encoding process according to ITU-T.81.
    It maintains all the tables and state needed for encoding.
    """
    
    def __init__(self, quality: int = 85):
        """
        Initialize JPEG encoder
        
        Args:
            quality: JPEG quality factor (1-100, higher = better quality)
        """
        self.encoding_core = CoreEncoder(quality)
    def encode_raw_image(self, img: np.array):
        """
        Encode a raw RGB image \n
        Args: img (np.array): raw RGB image
        """
        img_ycbcr = JPEGEncoder.rgb_2_ycbcr(img)

        img_y, img_cb, img_cr = JPEGEncoder.split_img(img_ycbcr)

        img_cb_sub = JPEGEncoder.chroma_subsample(img_cb,(4,2,2))
        img_cr_sub = JPEGEncoder.chroma_subsample(img_cr,(4,2,2))

        img_y_blocks = JPEGEncoder.divide_into_blocks(img_y)
        img_cb_blocks = JPEGEncoder.divide_into_blocks(img_cb_sub)
        img_cr_blocks = JPEGEncoder.divide_into_blocks(img_cr_sub)

        img_y_blocks_enc = self.encode_blocks(img_y_blocks, t_comp.Y)
        img_cb_blocks_enc = self.encode_blocks(img_cb_blocks, t_comp.Cb)
        img_cr_blocks_enc = self.encode_blocks(img_cr_blocks, t_comp.Cr)

        self.write_jpeg_file(img_y_blocks_enc, img_cb_blocks_enc, 
                             img_cr_blocks_enc, "my_image.jpeg")
    
    @staticmethod
    def rgb_2_ycbcr(img: np.array):
        """
        Encode a raw RGB image \n
        Args: img (np.array): raw RGB image \n
        Returns: img_ycbcr(np.array): image in YCBCR color space
        """
        t_matrix = np.array([
            [0.299, 0.587, 0.114],
            [-0.169, -0.331, 0.5],
            [0.5, -0.419, -0.081]
        ])

        img_ycbcr = img @ t_matrix.T

        img_ycbcr[:,:,1:3] += 128  # Cb & Cr offset
        img_ycbcr = np.round(np.clip(img_ycbcr, 0, 255))

        return img_ycbcr.astype(np.uint8)
    @staticmethod
    def split_img(img: np.array) -> tuple:
        """
        Splits a 3-D image into its 2-D component parts
        Ex. an RGB image -> (R_img, G_img, B_img)

        Args: img (np.array) : 3-D image \n
        Returns: img_tuple (tuple): a tuple of 2-D image components
        """
        return (img[:,:,0], img[:,:,1], img [:,:,2])
    
    @staticmethod
    def chroma_subsample(img_comp:np.array, sample_ratio: tuple):
        """
        Subsample a 2-D image \n
        Args: 
            img_comp (np.array): (assumed) Cb or Cr image
            sample_ratio (tuple): 3 member tuple expressing sample ratio \n
        Returns: img_comp_sub(np.array): subsampled image
        """
        if len(img_comp.shape) != 2:
            raise ValueError("input image component must be a 2-D shape")
        if img_comp.shape[0] % 4 != 0 or img_comp.shape[1] % 4 != 0:
            raise ValueError("input image component must have dimensions divisble by 4")
        
        if sample_ratio == (4,4,4): return img_comp

        height, width = img_comp.shape
        img_comp_sub = np.zeros(img_comp.shape,img_comp.dtype)
        for m in range(0,height,2):
            for n in range(0,width,4):
                img_comp_sub[m:m+2,n:n+4] = JPEGEncoder.block_chroma_subsample(img_comp[m:m+2,n:n+4], sample_ratio)    
        return img_comp_sub
    
    @staticmethod
    def block_chroma_subsample(block:np.array, sample_ratio: tuple) -> np.array:
        """
        Applies chroma subsampling to a 2 x 4 YCbCr block of pixels
        Parameters:
            block(np.ndarray) : a 2 x 4 matrix of Y, Cb, or Cr components
        Returns:
            block_sub(np.ndarray): a subsampled 2 x 4 Y, Cb, or Cr block
        """
        if sample_ratio not in [(4,4,4), (4,2,2), (4,2,0)]:
            raise ValueError("Only 4-4-4, 4-2-2, and 4-2-0 ratios are supported")
        
        if sample_ratio == (4,4,4): return block

        block_sub = np.zeros((2,4),block.dtype)
        for m in range(2):
            for n in range(0,4,2):
                # second row will either be half sampled or not sampled at all
                if(sample_ratio[2] == 2):
                    sample = block[m,n]
                else:
                    sample = block[0,n]
                block_sub[m,n] = block_sub[m,n+1] = sample
        return block_sub

    @staticmethod
    def divide_into_blocks(img_comp: np.array):
        """
        Divides a 2-D image into a list of 8 x 8 blocks \n
        Args: img_comp (np.array): 2-D image \n
        Returns: img_comp_block_list (np.array): list of 8 x 8 blocks
        """
        if len(img_comp.shape) != 2:
            raise ValueError("input image component must be a 2-D shape")
        
        h, w = img_comp.shape

        # handle image padding
        if h % 8 != 0 or w % 8 != 0:
            img_comp_i = JPEGEncoder.pad_image_comp(img_comp)
        else: img_comp_i = img_comp

        h_new, w_new = img_comp_i.shape
        img_comp_block_list = []
        for m in range(0,h_new,8):
            for n in range(0,w_new,8):
                img_comp_block_list.append(img_comp_i[m:m+8, n:n+8])
        return img_comp_block_list
    
    @staticmethod
    def pad_image_comp(img_comp:np.array) -> np.array:
        """
        Pad a 2D image so its height and width are divisible by 8\n
        Args: img_comp(np.array): a 2-D image\n
        Returns: img_comp_pad(np.array): input image with padded dimensions
        """
        orig_h, orig_w = h,w = img_comp.shape
        if h % 8 != 0:
            h = (h+(8-h%8))
        if w % 8 != 0:
            w = (w+(8-w%8))
        img_comp_pad = np.zeros((h,w), img_comp.dtype)
        img_comp_pad[0:orig_h, 0:orig_w] = img_comp[:,:]
        return img_comp_pad
    
    def encode_blocks(self, img_comp_blocks: list, comp_type: t_comp) -> list:
        """
        Encodes a list of raw 8 x 8 blocks using JPEG compression
        Args: 
            self (JPEGEncoder)
            img_comp_blocks (list): list of 8 x 8 YCbCr blocks\n
        Returns: 
            img_comp_blocks_enc (list): list of 1-D, huffman code arrays
        """
        img_comp_blocks_enc = []
        for block in img_comp_blocks:
            img_comp_blocks_enc.append(CoreEncoder.encode_block(block, comp_type))
        return img_comp_blocks_enc
    
    def write_jpeg_file(self, y_blocks_enc: list, cb_blocks_enc: list, 
                        cr_blocks_enc: list, output_file: string):
        """
        Generate a jpeg image file
        Args: 
            self (JPEGEncoder)
            y_blocks_enc (list): list of 1-D huffman code arrays for Luma (Y)
            cb_blocks_enc (list): list of 1-D huffman code arrays for Chroma Blue (Cb)
            cr_blocks_enc (list): list of 1-D huffman code arrays for Chroma Red (Cr)
            output_file (String): path for output image file
        """
        image_array = np.random.randint(0, 255, size=(100, 100, 3), dtype=np.uint8)
        cv2.imwrite(output_file, image_array)

# Usage Example
def main():
    img = cv2.imread("airplane.bmp")
    print(JPEGEncoder.rgb_2_ycbcr(img))
if __name__ == "__main__":
    main()
