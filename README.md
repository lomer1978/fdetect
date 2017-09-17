# fdetect
This is a project for detecting fractures from X-Ray images, using machine learning techniqes.

+++++++++++++
Data
+++++++++++++
The database consists of 170 samples, located in the data/ folder. Each sample is represented by 4 files:
    1. <sample_id>LT_Image.jpg - a lateral X-Ray image of a hand
    2. <sample_id>LT_Markings.txt - a text file describing circular markings of fractures on the LT_Image image.
       Each line of the file contains three numbers - x, y, R (x,y is the center of the circle in pixels, R is the radius)
       If the file is empty, no markings were made (an unfractured hand sample)
    3. <sample_id>AP_Image.jpg - an aposterior X-Ray image of the same hand
    4. <sample_id>AP_Markings.txt - markings of the fractures on the AP_Image file

+++++++++++++
Code
+++++++++++++
image_dim.py - utility function to calculate minimum and maximum ratios between AP and LT images in the sample set
image_dim2.py - utility function to calculate minimum and maximum dimensions in the sample set
gen_datasets.py - normalizes the dataset and uses data augmentation to generate a larger and normalized dataset in data2/.
                  The flow goes as follows:
                  - resize and stack both images of each sample to a single 224x224x2 array (one channel for AP and another for LT)
                  - normalize the labels. As the image was resized, the markings are now ellipses so each marking is represented
                    by four floats between 0 and 1. Exactly 4 markings are taken for each image (0 entries added if there are less
                    markings). So the entire label is now a a list 32 float number 0..1 (2 imagex * 4 markings * 4 floats per mark)
                  - 100 times:
                         - randomly flip the image
                         - randomly add brightness
                         - randomly add contrast
                         - randomly move the image

datview - a tool to view the images and markings from the augmented dataset (data2/)



