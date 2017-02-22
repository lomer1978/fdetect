import glob
import PIL
from PIL import Image
import numpy as np
import sys
import os

from six.moves import xrange  # pylint: disable=redefined-builtin
from six.moves import urllib

#from resnet_train import train
#from resnet import inference_small

IMAGE_SIZE=224
def normalize_images(file1, file2):
    dstsize = [IMAGE_SIZE, IMAGE_SIZE]
    img1 = Image.open(file1)
    img1=img1.resize(dstsize, PIL.Image.ANTIALIAS)
    img2 = Image.open(file2)
    img2=img2.resize(dstsize, PIL.Image.ANTIALIAS)
    data1 = np.ascontiguousarray(np.fromstring(img1.tobytes(), dtype=np.uint8).reshape(img1.size+(3,))[:,:,1], dtype=np.uint8)
    data2 = np.ascontiguousarray(np.fromstring(img2.tobytes(), dtype=np.uint8).reshape(img2.size+(3,))[:,:,1], dtype=np.uint8)
    return np.stack((data1, data2),2), dstsize, dstsize

def normalize_label(file, size):
    s=""
    fd=open(file, "r")
    for i in range(4):
        list=fd.readline().split();
        if len(list) != 3 or list[2] < 3:
            s+= "0 0 0 0 "
        else:
            s+= str(float(list[0])/float(size[0])) + " " + str(float(list[1])/float(size[1])) + " " + str(float(list[2])/float(size[0])) + " " + str(float(list[2])/float(size[1])) + " "
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

            fd = open(f.replace(srcpath, dstpath).replace("AP_Image.jpg", "Lbl.txt"), "wb")
            fd.write(newaplbl + newltlbl)
            fd.close()

            sys.stdout.write('\r>> converting %s %.1f%%' %
                             (srcpath, float(count) /
                              float(total_size) * 100.0))
            sys.stdout.flush()
        print
        fd=open(dstpath+"converted", "wb")
        fd.close()

maybe_convert_dataset("data/", "data2/")

