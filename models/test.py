import unittest
import numpy as np
import cv2
from jpegEncoder import JPEGEncoder

class TestColorConvMethod(unittest.TestCase):

    def ycrcb_2_ycbcr(self, img:np.array):
        img_ycbcr = np.zeros(img.shape, img.dtype)
        img_ycbcr[:,:,0] = img[:,:,0]
        img_ycbcr[:,:,1] = img[:,:,2]
        img_ycbcr[:,:,2] = img[:,:,1]
        return img_ycbcr
    def test_blank(self):
        blank_img = np.random.randint(255,256,(512,256,3),np.uint8)
        img_exp = cv2.cvtColor(blank_img, cv2.COLOR_RGB2YCrCb)
        img_res = JPEGEncoder.rgb_2_ycbcr(blank_img)
        self.assertTrue(np.array_equal(img_exp,img_res))
    
    def test_solid(self):
        solid_img = np.random.randint(0,1,(256,256,3),np.uint8)
        img_exp = cv2.cvtColor(solid_img, cv2.COLOR_RGB2YCrCb)
        img_res = JPEGEncoder.rgb_2_ycbcr(solid_img)
        self.assertTrue(np.array_equal(img_exp,img_res))
    
    def test_rand(self):
        rand_img = np.random.randint(0,256,(1024,512,3), np.uint8)
        img_exp = self.ycrcb_2_ycbcr(cv2.cvtColor(rand_img, cv2.COLOR_RGB2YCrCb))
        img_res = JPEGEncoder.rgb_2_ycbcr(rand_img)
        # convert to int16 to avoid underflow due to a -1 result from subtaction
        self.assertTrue(np.all(np.abs(img_exp.astype(np.int16) - img_res.astype(np.int16)) <= 1))

class TestSplitImageMethod(unittest.TestCase):
    def test_split_img(self):
         rand_img = np.random.randint(0,256,(1024,512,3), np.uint8)
         y_res, cb_res, cr_res = JPEGEncoder.split_img(rand_img)
         self.assertTrue(np.array_equal(rand_img[:,:,0],y_res))
         self.assertTrue(np.array_equal(rand_img[:,:,1],cb_res))
         self.assertTrue(np.array_equal(rand_img[:,:,2],cr_res))

class TestChromaSubSampleMethod(unittest.TestCase):
    def test_444(self):
         rand_img_comp = np.random.randint(0,256,(2,4), np.uint8)
         img_comp_res = JPEGEncoder.block_chroma_subsample(rand_img_comp,(4,2,0))
         print(rand_img_comp)
         print(img_comp_res)
        #  self.assertTrue(np.array_equal(rand_img_comp[:,:,0],img_comp_res))
    
if __name__ == '__main__':
    unittest.main()
