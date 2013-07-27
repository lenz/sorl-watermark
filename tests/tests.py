# -*- coding: utf-8 -*-

from django.conf import settings
import unittest
from PIL import Image as PILImage

settings.configure(THUMBNAIL_WATERMARK = 'mark.png',
                   STATICFILES_DIRS = ('src/', ), )

# importing Engine after configuring django.conf.settings
from sorl_watermarker.engines.pil_engine import Engine as PILEngine



class PILTestCase(unittest.TestCase):

    def setUp(self):
        self.bg = PILImage.open('src/bg.png')
        self.engine = PILEngine()
        self.img_dir = 'src/control_instances/pngs/watermark_pos/'

    def get_pixels_list(self, image, denom=1000):
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        image_pixels = list(image.getdata())
        short_list = [pixel for loop, pixel in enumerate(image_pixels)
                      if loop%denom == 0]
        return short_list

    def position(self, position='default'):
        print 'Testing position: ' + position
        pre_image = PILImage.open(self.img_dir + position + '.png')
        if position == 'default':
            options = dict()
        else:
            options = {'watermark_pos': position}
        mark = self.engine.watermark(self.bg, options)
        self.assertEqual(self.get_pixels_list(mark), self.get_pixels_list(pre_image))


    def runTest(self):
        self.position()
        self.position('center')
        self.position('south east')
        self.position('south west')
        self.position('north east')
        self.position('north west')
        self.position('50 50')
        self.position('50 -50')
        self.position('-50 -50')
        self.position('-50 50')

if __name__ == '__main__':
    unittest.main()

