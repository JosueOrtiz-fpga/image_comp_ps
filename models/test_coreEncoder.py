import unittest
import numpy as np
import math
from coreEncoder import CoreEncoder, t_comp

class TestEncodeBlockMethod(unittest.TestCase):
    def test_encode_block(self):
        rand_block = np.random.randint(0,256,(8,8), np.uint8)
        core = CoreEncoder()
        block_enc = core.encode_block(rand_block, t_comp.Y)
        self.assertTrue(np.array_equal(block_enc, np.zeros(64,rand_block.dtype)))
    def test_dct2(self):
        zero_block = np.random.randint(0,1,(8,8), np.uint8)
        block_enc = CoreEncoder.dct2(8,zero_block)
        self.assertTrue(np.array_equal(block_enc,np.zeros((8,8),np.uint8)))
    def test_quant(self):
        zero_block = np.random.randint(0,1,(8,8), np.uint8)
        core = CoreEncoder()
        block_enc = core.quant(zero_block, t_comp.Y)
        self.assertTrue(np.array_equal(block_enc,np.zeros((8,8),np.uint8)))
    def test_zigzag(self):
        zero_block = np.random.randint(0,1,(8,8), np.uint8)
        block_enc = CoreEncoder.zigzag_scan(zero_block)
        self.assertTrue(np.array_equal(block_enc,np.zeros(64,np.uint8)))
    def test_rle(self):
        ones = np.random.randint(1,2,4, np.uint8)
        block_enc = CoreEncoder.rle(ones)
        block_exp = [(0,item, math.log2(item)+1) for item in ones]
        self.assertTrue(np.array_equal(block_enc,block_exp))
    def test_huff(self):
        zeros = np.random.randint(0,1,8,np.uint8)
        core = CoreEncoder()
        block_enc = core.huffman_encode(zeros)
        block_exp = [(0,0) for i in zeros]
        self.assertTrue(np.array_equal(block_enc,block_exp))

if __name__== "__main__":
    unittest.main()
