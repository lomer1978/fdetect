import glob
import PIL
from PIL import Image
import numpy as np
import sys
import os

from six.moves import xrange  # pylint: disable=redefined-builtin
from six.moves import urllib

from resnet_train import train
from resnet import inference_small

def normalize_images(file1, file2):
    img1 = Image.open(file1)
    img2 = Image.open(file2)
    img2=img2.resize(img1.size, PIL.Image.ANTIALIAS)
    data1 = np.ascontiguousarray(np.fromstring(img1.tobytes(), dtype=np.uint8).reshape(img1.size+(3,))[:,:,1], dtype=np.uint8)
    data2 = np.ascontiguousarray(np.fromstring(img2.tobytes(), dtype=np.uint8).reshape(img1.size+(3,))[:,:,1], dtype=np.uint8)
    return np.stack((data1, data2),2), img1.size, img2.size

def normalize_label(file, size):
    s=""
    fd=open(file, "r")
    while True:
        list=fd.readline().split();
        if len(list) != 3:
            break
        s+= str(float(list[0])/float(size[0]))+" "
        s+= str(float(list[1])/float(size[1]))+" "
        s+= str(float(list[2])/float(size[0]))+" "
        s+= str(float(list[2])/float(size[1]))+"\n"
    fd.close()
    return s

def maybe_convert_dataset(srcpath, dstpath):
    if not os.path.exists(dstpath+"converted"):
        filelist=glob.glob(srcpath+"/*AP_Image.jpg")
        count=0
        total_size=len(filelist)
        for f in filelist:
            count=count+1
            apfile = f
            ltfile = f.replace("AP_Image.jpg", "LT_Image.jpg")
            aplfile = f.replace("AP_Image.jpg", "AP_Markings.txt")
            ltlfile = f.replace("AP_Image.jpg", "LT_Markings.txt")
            (newimage, apsize, ltsize) = normalize_images(apfile, ltfile)
            
            newaplbl = normalize_label(aplfile, apsize)
            newltlbl = normalize_label(ltlfile, ltsize)
            
            fd = open(f.replace(srcpath, dstpath).replace("AP_Image.jpg", "Image.dat"), "wb")
            fd.write(newimage)
            fd.close()

            fd = open(ltlfile.replace(srcpath, dstpath), "wb")
            fd.write(newltlbl)
            fd.close()

            fd = open(aplfile.replace(srcpath, dstpath), "wb")
            fd.write(newaplbl)
            fd.close()

            sys.stdout.write('\r>> converting %s %.1f%%' %
                             (srcpath, float(count) /
                              float(total_size) * 100.0))
            sys.stdout.flush()
        print
        fd=open(dstpath+"converted", "wb")
        fd.close()

maybe_convert_dataset("data/", "data2/")

