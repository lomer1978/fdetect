import scipy
from scipy import misc
import glob

minx=8000
miny=8000
maxx=0
maxy=0
filelist = glob.glob("data/*AP_Image.jpg")
for ap in filelist:
    lt = ap.replace("AP", "LT")
    im1s = [ float(t) for t in scipy.misc.imread(ap).shape ]
    im2s = [ float(t) for t in scipy.misc.imread(lt).shape ]

    minx=min(im1s[0]/im2s[0], minx)
    miny=min(im1s[1]/im2s[1], miny)
    maxx=max(im1s[0]/im2s[0], maxx)
    maxy=max(im1s[1]/im2s[1], maxy)
    print (im1s, im2s, im1s[0]/im2s[0], im1s[1]/im2s[1])

print ("max:", maxx, maxy)
print ("min:", minx, miny)
