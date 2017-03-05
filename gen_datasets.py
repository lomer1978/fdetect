import glob
import PIL
from PIL import Image
import numpy as np
from scipy.ndimage.interpolation import shift
import sys
import os
import random
import string

IMAGE_SIZE=224

def normalize_images(file1, file2):
    dstsize = [IMAGE_SIZE, IMAGE_SIZE]
    img1 = Image.open(file1)
    sz1 = img1.size
    img1=img1.resize(dstsize, PIL.Image.ANTIALIAS)
    img2 = Image.open(file2)
    sz2 = img2.size
    img2=img2.resize(dstsize, PIL.Image.ANTIALIAS)
    data1 = np.ascontiguousarray(np.fromstring(img1.tobytes(), dtype=np.uint8).reshape(img1.size+(3,))[:,:,1], dtype=np.uint8)
    data2 = np.ascontiguousarray(np.fromstring(img2.tobytes(), dtype=np.uint8).reshape(img2.size+(3,))[:,:,1], dtype=np.uint8)
    return np.stack((data1, data2),2), sz1, sz2

def rnd_flip(img, lbl):
    newlbl = lbl
    if random.randint(1,2) == 1:
        newimg = np.ascontiguousarray(np.fliplr(img))
        for i in range(0, len(lbl), 4):
            if lbl[i] != 0 and lbl[i+1] != 0: #valid entry
                newlbl[i] = 1 - newlbl[i]
    else:
        newimg = img
                
    return (newimg, newlbl)

def rnd_contrast(img, lbl):
    newlbl = lbl
    mean=np.mean(img)
    contrast = random.uniform(0.2, 0.8)
    newimg = ((img - mean)*contrast + mean).clip(0, 255)
    return  (newimg, newlbl)

def rnd_brightness(img, lbl):
    newlbl = lbl
    brightness=random.randint(0, 63)
    newimg = (img+brightness).clip(0, 255)
    return (newimg, newlbl)

def rnd_move(img, lbl):
    newlbl = lbl
    dx = random.randint(-7, 7)
    dy = random.randint(-7, 7)
    newimg = shift(img, [dx, dy, 0])
    for i in range(0, len(lbl), 4):
        if lbl[i] != 0 and lbl[i+1] != 0:
            newlbl[i] = newlbl[i]+dx
            newlbl[i+1] = newlbl[i+1]+dy
        
    return (newimg, newlbl)

def standardize(img):
    mean = np.mean(img)
    stddev = max(np.std(img), 1.0/np.sqrt(img.size))
    newimg = img-mean/stddev
    return newimg
    
    
def normalize_label(file, size):
    s=[]
    fd=open(file, "r")
    for i in range(4):
        list=fd.readline().split();
        if len(list) != 3 or list[2] < 3: #ignore small radius markings
            s+= [0, 0, 0, 0]
        else:
            s+= [float(list[0])/float(size[0]), float(list[1])/float(size[1]), float(list[2])/float(size[0]), float(list[2])/float(size[1])]
    fd.close()
    return s

AUG_PER_SAMPLE=10

def flist2str(flist):
    return string.join([str(f) for f in flist])
        
def maybe_convert_dataset(srcpath, dstpath):
    random.seed()
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
            newimage = standardize(newimage)
            
            newaplbl = normalize_label(aplfile, apsize)
            newltlbl = normalize_label(ltlfile, ltsize)
            
            fd = open(f.replace(srcpath, dstpath).replace("AP_Image.jpg", "Image.dat"), "wb")
            fd.write(newimage)
            fd.close()

            fd = open(f.replace(srcpath, dstpath).replace("AP_Image.jpg", "Lbl.txt"), "wb")
            fd.write(flist2str(newaplbl + newltlbl))
            fd.close()

            for i in range(AUG_PER_SAMPLE):
                (augimage, auglabel) = rnd_flip(newimage, newaplbl + newltlbl)
                (augimage, auglabel) = rnd_brightness(augimage, auglabel)
                (augimage, auglabel) = rnd_contrast(augimage, auglabel)
                (augimage, auglabel) = rnd_move(augimage, auglabel)
                augimage = standardize(augimage)
                
                fd = open(f.replace(srcpath, dstpath).replace("AP_Image.jpg", "Image-"+str(i)+".dat"), "wb")
                fd.write(augimage)
                fd.close()

                fd = open(f.replace(srcpath, dstpath).replace("AP_Image.jpg", "Lbl-"+str(i)+".txt"), "wb")
                fd.write(flist2str(auglabel))
                fd.close()

                
            sys.stdout.write('\r>> converting %s %.1f%%' %
                             (srcpath, float(count) /
                              float(total_size) * 100.0))
            sys.stdout.flush()
        print
        fd=open(dstpath+"converted", "wb")
        fd.close()

maybe_convert_dataset("data/", "data2/")

