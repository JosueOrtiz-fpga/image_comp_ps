"""
JPEG Baseline Encoder - Complete Template
Based on ITU-T.81 Standard

This template shows the high-level structure of our JPEG encoder implementation.
We'll build each component step by step.
"""

import numpy as np
import string
from enum import Enum
import cv2

#---------------
# Constants

STD_LUMA_QUANT_TABLE = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                [12, 12, 14, 19, 26, 58, 60, 55],
                                [14, 13, 16, 24, 40, 57, 69, 56],
                                [14, 17, 22, 29, 51, 87, 80, 62],
                                [18, 22, 37, 56, 68, 109, 103, 77],
                                [24, 35, 55, 64, 81, 104, 113, 92],
                                [49, 64, 78, 87, 103, 121, 120, 101],
                                [72, 92, 95, 98, 112, 100, 103, 99]], dtype=np.uint16)

STD_CHROMA_QUANT_TABLE = np.array([[17, 18, 24, 47, 99, 99, 99, 99],
                                [18, 21, 26, 66, 99, 99, 99, 99],
                                [24, 26, 56, 99, 99, 99, 99, 99],
                                [47, 66, 99, 99, 99, 99, 99, 99],
                                [99, 99, 99, 99, 99, 99, 99, 99],
                                [99, 99, 99, 99, 99, 99, 99, 99],
                                [99, 99, 99, 99, 99, 99, 99, 99],
                                [99, 99, 99, 99, 99, 99, 99, 99]], dtype=np.uint16)

STD_LUMA_DC_HUFF_BITS = [0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
STD_LUMA_DC_HUFF_VALS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

STD_CHROMA_DC_HUFF_BITS = [0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
STD_CHROMA_DC_HUFF_VALS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

STD_LUMA_AC_HUFF_BITS = [0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 125]
STD_LUMA_AC_HUFF_VALS = [0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 
                        0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07, 0x22, 0x71, 
                        0x14, 0x32, 0x81, 0x91, 0xa1, 0x08,0x23, 0x42, 0xb1, 
                        0xc1, 0x15, 0x52, 0xd1, 0xf0, 0x24, 0x33, 0x62, 0x72,
                        0x82, 0x09, 0x0a, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x25, 
                        0x26, 0x27, 0x28, 0x29, 0x2a, 0x34, 0x35, 0x36, 0x37, 
                        0x38, 0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 
                        0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
                        0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 
                        0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x83, 
                        0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a, 0x92, 0x93, 
                        0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3,
                        0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 
                        0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3, 
                        0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xd2, 0xd3, 
                        0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xe1, 0xe2,
                        0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xf1, 
                        0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa]

STD_CHROMA_AC_HUFF_BITS = [0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 119]
STD_CHROMA_AC_HUFF_VALS = [
        0x00, 0x01, 0x02, 0x03, 0x11, 0x04, 0x05, 0x21, 0x31, 0x06, 0x12, 0x41, 
        0x51, 0x07, 0x61, 0x71, 0x13, 0x22, 0x32, 0x81, 0x08, 0x14, 0x42, 0x91, 
        0xa1, 0xb1, 0xc1, 0x09, 0x23, 0x33, 0x52, 0xf0, 0x15, 0x62, 0x72, 0xd1, 
        0x0a, 0x16, 0x24, 0x34, 0xe1, 0x25, 0xf1, 0x17, 0x18, 0x19, 0x1a, 0x26, 
        0x27, 0x28, 0x29, 0x2a, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x43, 0x44, 
        0x45, 0x46, 0x47, 0x48, 0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 
        0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x73, 0x74, 
        0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 
        0x88, 0x89, 0x8a, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 
        0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4, 
        0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, 
        0xc8, 0xc9, 0xca, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 
        0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xf2, 0xf3, 0xf4, 
        0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa
    ]

#---------------
# DataTypes

class ComponentType(Enum):
    """Image component types"""
    Y = "luminance"
    CB = "chrominance_blue"
    CR = "chrominance_red"

class QuantizationTable:
    """Quantization table container"""
    def __init__(self, table_data: np.ndarray, table_id: int = 0):
        self.data = table_data.astype(np.uint16)  # 8x8 quantization values
        self.table_id = table_id
    
    @staticmethod
    def std_luma_table():
        """Standard quantization table from ITU-T81 for luma coefficients"""
        return STD_LUMA_QUANT_TABLE
        
    @staticmethod
    def std_chroma_table():
        """Standard quantization table from ITU-T81 for luma coefficients"""
        return STD_CHROMA_QUANT_TABLE

class HuffmanTable:
    """Huffman coding table"""
    def __init__(self, table_type: str, huff_bits: np.array, huff_vals: np.array, table_id: int = 0):
        self.table_type = table_type  # 'DC' or 'AC'
        self.table_id = table_id
        self.huff_bits = huff_bits
        self.huff_vals = huff_vals
        self.codes = HuffmanTable.gen_huff_dict(huff_bits, huff_vals)
    
    @classmethod
    def std_luma_dc_table(cls):
        """Standard huffman codes from ITU-T81 for dc luma encoding"""
        huff_table = cls("DC",STD_LUMA_DC_HUFF_BITS, STD_LUMA_DC_HUFF_VALS)
        return huff_table
        
    @classmethod
    def std_luma_ac_table(cls):
        """Standard huffman codes from ITU-T81 for ac luma encoding"""
        huff_table = cls("AC",STD_LUMA_AC_HUFF_BITS, STD_LUMA_AC_HUFF_VALS)
        return huff_table
    
    @classmethod
    def std_chroma_dc_table(cls):
        """Standard huffman codes from ITU-T81 for dc chroma encoding"""
        huff_table = cls("DC",STD_CHROMA_DC_HUFF_BITS, STD_CHROMA_DC_HUFF_VALS)
        return huff_table
    
    @classmethod
    def std_chroma_ac_table(cls):
        """Standard huffman codes from ITU-T81 for ac chroma encoding"""
        huff_table = cls("AC",STD_CHROMA_AC_HUFF_BITS, STD_CHROMA_AC_HUFF_VALS)
        return huff_table

    @staticmethod
    def gen_huff_dict(huff_bits: np.array, huff_vals: np.array) -> dict:
        """
        Generate Huffman codes from BITS and HUFFVAL arrays.
    
        Args:
        huff_bits: 16-element array specifying number of codes of each length
        huff_vals: Array of values (symbols) assigned to codes
    
        Returns:
        dict: Dictionary where key is the value/symbol and value is a tuple (code, size)
              huffman_dict[symbol] = (huffman_code, code_length)
        """
    
        # Step 1: Generate HUFFSIZE table
        huffsize = []
        for code_length in range(1, 17):  # Lengths 1-16
            count = huff_bits[code_length - 1]
            for _ in range(count):
                huffsize.append(code_length)
        huffsize.append(0)  # Terminator
    
        # Step 2: Generate HUFFCODE table
        huffcode = []
        code = 0
        si = huffsize[0] if huffsize else 0
    
        for i, size in enumerate(huffsize[:-1]):  # Exclude terminator
            while size > si:
                code = code << 1
                si += 1
            huffcode.append(code)
            code += 1
    
    # Step 3: Create lookup dictionary
        huffman_dict = {}
        for i, value in enumerate(huff_vals):
            huffman_dict[value] = (huffcode[i], huffsize[i])
    
        return huffman_dict

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
        self.quality = quality
        
        # Initialize quantization tables
        self.quant_tables = {
            ComponentType.Y: QuantizationTable.std_luma_table(),
            ComponentType.CB: QuantizationTable.std_chroma_table(),
            ComponentType.CR: QuantizationTable.std_chroma_table()
        }
        
        # Initialize Huffman tables
        self.huffman_dc_tables = {
            ComponentType.Y: HuffmanTable.std_luma_dc_table(),
            ComponentType.CB: HuffmanTable.std_chroma_dc_table(),
            ComponentType.CR: HuffmanTable.std_chroma_dc_table()
        }
        
        self.huffman_ac_tables = {
            ComponentType.Y: HuffmanTable.std_luma_ac_table(),
            ComponentType.CB: HuffmanTable.std_chroma_dc_table(),
            ComponentType.CR: HuffmanTable.std_chroma_dc_table(),
        }
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

        img_y_blocks_enc = self.encode_blocks(img_y_blocks)
        img_cb_blocks_enc = self.encode_blocks(img_cb_blocks)
        img_cr_blocks_enc = self.encode_blocks(img_cr_blocks)

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
                for i in range(4):
                    img_comp_sub[m,n+i] = img_comp[m,n+(2*int(i/2))]
                    img_comp_sub[m+1,n+i] = img_comp
                # second row handling
                n + m
                    
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
        # first row will only support half-subsampling
        block_sub[0] = [block[0,0],block[0,0],block[0,2],block[0,2]]
        # second row, either half or no subsampled
        if sample_ratio[2] == 2: block_sub[1] = [block[1,0],block[1,0],block[1,2],block[1,2]]
        else: block_sub[1] = block_sub[0]

        return block_sub

    @staticmethod
    def divide_into_blocks(img_comp: np.array):
        """
        Divides a 2-D image into a list of 8 x 8 blocks \n
        Args: img_comp (np.array): 2-D image \n
        Returns: img_comp_block_list (np.array): list of 8 x 8 blocks
        """

        img_comp_block_list = []
        for i in range(img_comp.shape[0]):
            img_comp_block_list.append(np.zeros((8,8), np.uint8))
        return img_comp_block_list
    
    def encode_blocks(self, img_comp_blocks: list):
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
            img_comp_blocks_enc.append(np.random.randint(0,255,64,np.uint8))
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
