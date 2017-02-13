import scipy
from scipy import misc
import glob

min0=8000
min1=8000
min2=8000
max0=0
max1=0
max2=0
filelist = glob.glob("data/*Image.jpg")
dimlist = [ scipy.misc.imread(f).shape for f in filelist ]

max = [ max(e[i] for e in dimlist) for i in range(0,3) ]
min = [ min(e[i] for e in dimlist) for i in range(0,3) ]

print ("max:", max)
print ("min:", min)
