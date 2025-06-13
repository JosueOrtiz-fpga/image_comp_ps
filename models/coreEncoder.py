import numpy as np
from enum import Enum
#---------------
# Constants



# constant defining functions

# DCT Transform Matrix
def dct2_mat(n:np.uint) -> np.array:
    """
    Returns an n x n DCT tranform matrix
    Parameters:
        n(uint): matrix dimension desired
    Returns:
        mat(np.array): An n x n DCT transform matrix 
    """
    mat = np.zeros((n,n))
    for p in range(n):
        for q in range(n):
            if p ==0:
                mat[p,q] = 1/np.sqrt(n)
            else:
                mat[p,q] = np.sqrt(2/n) * np.cos((np.pi*(2*q+1)*p)/(2*n))
    return mat

# Huffman Codes Dictionary
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
STD_LUMA_DC_HUFF_DICT = gen_huff_dict(STD_LUMA_DC_HUFF_BITS, STD_LUMA_DC_HUFF_VALS)

STD_CHROMA_DC_HUFF_BITS = [0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
STD_CHROMA_DC_HUFF_VALS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
STD_CHROMA_DC_HUFF_DICT = gen_huff_dict(STD_CHROMA_DC_HUFF_BITS, STD_CHROMA_DC_HUFF_VALS)

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
STD_LUMA_AC_HUFF_DICT = gen_huff_dict(STD_LUMA_AC_HUFF_BITS, STD_LUMA_AC_HUFF_VALS)

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
STD_CHROMA_AC_HUFF_DICT = gen_huff_dict(STD_CHROMA_AC_HUFF_BITS, STD_CHROMA_AC_HUFF_VALS)

#---------------
# DataTypes

t_comp = Enum('t_comp', [("Y", "Luma"), ("Cb", "Chroma_B"), ("Cr", "Chroma_R")])


#----------
# Core Encoder
# ---------

class CoreEncoder:
    def __init__(self, quality: int = 85):
        """
        Initialize JPEG encoder
        
        Args:
            quality: JPEG quality factor (1-100, higher = better quality)
        """
        self.quality = quality
        
        # Initialize quantization tables
        self.quant_tables = {
            t_comp.Y: STD_LUMA_QUANT_TABLE,
            t_comp.Cb: STD_CHROMA_QUANT_TABLE,
            t_comp.Cr: STD_CHROMA_QUANT_TABLE
        }
        
        # Initialize Huffman tables
        self.huffman_dc_tables = {
            t_comp.Y: STD_LUMA_DC_HUFF_DICT,
            t_comp.Cb: STD_CHROMA_DC_HUFF_DICT,
            t_comp.Cr: STD_CHROMA_DC_HUFF_DICT
        }
        
        self.huffman_ac_tables = {
            t_comp.Y: STD_LUMA_AC_HUFF_DICT,
            t_comp.Cb: STD_CHROMA_AC_HUFF_DICT,
            t_comp.Cr: STD_CHROMA_AC_HUFF_DICT,
        }
    def encode_block(self,block:np.array, block_type:t_comp) -> np.array:
        """
        Encode an 8 x 8 YCbCr block using JPEG compression
        Args: block(np.array) : 2-D array
        Returns: block_enc(np.array) : 1-D array
        """
        if block.shape != (8,8):
            raise TypeError("Input block must be an 8 x 8 matrix")
        
        block_dct = CoreEncoder.dct2(8, block)
        block_dct_quant = self.quant(block_dct, block_type)
        block_dct_quant_zz = self.zigzag_scan(block_dct_quant)
        return np.array(block).flatten("C")
    
    @staticmethod
    def dct2(n:np.uint, block: np.array) -> np.array:
        """
        Perform the 2-D DCT of an n x n matrix
        Args: 
            n (np.uint): square dimension of block input
            block (np.array): block input
        Returns:
            block_dct2 (np.array): 2D DCT of block input
        """
        if block.shape[0] != block.shape[1]:
            raise TypeError("Input block must be a square matrix")
        
        t_matrix = dct2_mat(n)

        return t_matrix @ block @ t_matrix.T
    
    def quant(self, block:np.array, block_type: t_comp) -> np.array:
        """
        Quantize a 8 x 8 block of Luma or Chroma DCT coefficients
        Args:
            block (np.array): 8 x 8 input block
            block_type (t_comp): component type, Luma or Chroma
        Return:
            block_quant (np.array): 8 x 8 quantized block
        """
        return block // self.quant_tables[block_type]
    
    @staticmethod
    def zigzag_scan(block : np.array) -> np.array:
        """
        Flattens and reorders a 2-D, 8 x 8 array\n
        Args: block (np.array): 8 x 8 input block\n
        Return: block_zz (np.array) : 1 x 64 array
        """
        index_order = np.array([
            [0, 1, 5, 6,14,15,27,28],
            [2, 4, 7,13,16,26,29,42],
            [3, 8,12,17,25,30,41,43],
            [9,11,18,24,31,40,44,53],
            [10,19,23,32,39,45,52,54],
            [20,22,33,38,46,51,55,60],
            [21,34,37,47,50,56,59,61],
            [35,36,48,49,57,58,62,63]
            ]).flatten("C")
        return block.flatten("C")[index_order]
        
