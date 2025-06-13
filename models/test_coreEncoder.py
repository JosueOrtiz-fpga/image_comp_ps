import unittest
import numpy as np
from coreEncoder import CoreEncoder, t_comp

class TestEncodeBlockMethod(unittest.TestCase):
    def test_shape(self):
        rand_block = np.random.randint(0,256,(8,8), np.uint8)
        core = CoreEncoder()
        block_enc = core.encode_block(rand_block, t_comp.Y)
        self.assertTrue(len(block_enc.shape) == 1)
    
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

if __name__== "__main__":
    unittest.main()
