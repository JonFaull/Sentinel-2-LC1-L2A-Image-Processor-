import rasterio
from rasterio import plot
from rasterio import merge
import matplotlib
import matplotlib.pyplot as plt 
import numpy as np
import glob
import os
from sys import getsizeof
from rasterio.plot import show
import sys
import gc 
import pygeoj
import fnmatch
import re


print(np.intp)
gc.enable()

def GetBand(BandName, ImagePath): #Function to locate and open the image .jp2 bands
    
    print('Bandname:', BandName)
    print('ImagePath0:', ImagePath[0])
    
    nameRegex = re.compile(r'R10m')
    R10 = nameRegex.findall(ImagePath[0])
    print(R10)

    if re.search(r'R10m', ImagePath[0]):
        print(True)
    else:
        print(False)
    

    if re.search(r'R10m', ImagePath[0]):
        print('R10m')
        if 2 <= BandName <= 4:
            x = BandName - 1
        elif BandName == 8:
            x = 4
        elif BandName == 'WVP':
            x = 6
        elif BandName == 'AOT':
            x = 0
            
        print('bandname =', BandName)
        print('x =', x)
    elif re.search(r'R20m', ImagePath[0]):
        print('R20m')
        if 1 <= BandName <= 8:
            x = BandName - 1
        elif BandName == '11':
            x = 8
        elif BandName == '12':
            x = 9
        elif BandName == 'SCL':
            x = 10
        elif BandName == 'WVP':
            x = 11
        elif BandName == 'AOT':
            x = 0
        print('bandname =', BandName)
        print('x =', x)

    elif re.search(r'R60m', ImagePath[0]):
        print('R60m')
        if 1 <= BandName <= 9:
            x = BandName
        elif BandName == '11':
            x = 10        
        elif BandName == '12':
            x = 11
        elif BandName == 'SCL':
            x = 12
        elif BandName == 'WVP':
            x = 14
        elif BandName == 'AOT':
            x = 0

        print('bandname =',BandName)
        print('x =', x)
    else: 
        print('L1C')
        if isinstance(BandName, int) == True:
            x = BandName - 1
        elif BandName == '8A':
            x = 12
        elif BandName == 'PVI':
            x = 13   
        else: 
            BandName = -1
        print('bandname =', BandName)
        print('x =', x)
        
    print(x)

    BandPath = ImagePath[x]
    print(BandPath)
    
    band = rasterio.open(BandPath) #driver='JP2OpenJPEG')
    return band
    



def TrueColourImg(SAVE_Location): #Funcion to create a true colour image our of red, blue and green channels.
    
    saveLocationName = SAVE_Location + 'True_Colour_Image_' + resolutionName + '.tiff'
    

    truecolor = rasterio.open(saveLocationName,'w', driver = 'Gtiff',
            width = band4.width, height = band4.height,
            count = 3,
            crs = band4.crs,
            transform = band4.transform,
            dtype = 'uint16' #band4.dtypes[0] 
            )

    band2_new = band2.read(1)
    band3_new = band3.read(1)
    band4_new = band4.read(1)
    band8_new = band8.read(1)



    
    
    truecolor.write(band4_new,1) #Red #Indicates the order in which bands should be written, RGB: 1, 2, 3. Other wise your image will not be true colour. 
    truecolor.write(band3_new,2) #Green     
    truecolor.write(band2_new,3) #Blue

    truecolor.close()
    print("True Colour Created")

def FalseColourRedImg(SAVE_Location): #Funcion to create a False colour image our of red, blue and green channels.
    
    saveLocationName = SAVE_Location + 'False_Colour_Image_' + resolutionName + '.tiff'
    
    falseColor = rasterio.open(saveLocationName,'w', driver = 'Gtiff',
            width = band4.width, height = band4.height,
            count = 3,
            crs = band4.crs,
            transform = band4.transform,
            dtype = 'uint16' #band4.dtypes[0] 
            )
    band2_new = band2.read(1)
    band3_new = band3.read(1)
    band4_new = band4.read(1)
    band8_new = band8.read(1)


    falseColor.write(band8_new,1) #Blue
    falseColor.write(band4_new,2) #Green     
    falseColor.write(band3_new,3) #Red

    falseColor.close()
    print("False Colour [Vegetation] Created")

def NormalizedDifferenceVegetationIndex(SAVE_Location): #Funcion to create a False colour image our of red, blue and green channels.
    
    saveLocationName = SAVE_Location + 'NDVI_' + resolutionName + '.tiff'
    
    NDVI_Image = rasterio.open(saveLocationName,'w', driver = 'Gtiff',
            width = band4.width, height = band4.height,
            count = 3,
            crs = band4.crs,
            transform = band4.transform,
            dtype = 'float64', #band4.dtypes[0] #'uint16'
            compress = 'lzw'
            )
    
    band4_new = band4.read(1)
    band8_new = band8.read(1)
    
    TOP = band8_new.astype(int) - band4_new.astype(int)
    BOTTOM = band8_new.astype(int) + band4_new.astype(int)


    print(band4_new)
    print(band8_new)
    print(TOP)
    print(BOTTOM)
    
    NDVI_Values = (TOP.astype(int))/(BOTTOM.astype(int))
    NDVI_Values = np.around(NDVI_Values, decimals = 3)

    #b = int(band8_new) - (band4_new)
    #c = (band8_new + band4_new)
    
    #d = b/c
    print(NDVI_Values)
    #print(c)
    #print(d)
    
    NDVI_Values.astype('uint16')

    NDVI = np.array(NDVI_Values, dtype = float) 
    
    t = getsizeof(NDVI)
    
    del NDVI_Values
    print(t)
    print(NDVI)
    
    #NDVI = NDVI.read(1)

    #print(NDVI)

    NDVI_Image.write(NDVI,1)
    NDVI_Image.write(NDVI,2)
    NDVI_Image.write(NDVI,3) #Blue
    #falseColor.write(band4_new,2) #Green     
    #falseColor.write(band3_new,3) #Red

    NDVI_Image.close()
    print("NDVI Created")

    del NDVI


ProjectName = '2018-6-1 - 2018-7-10_Donegal_30_L2A'
projectFolder = 'E:/Products/'

Cropped_Image_Location = projectFolder + ProjectName + '/*'

projectFolder = glob.glob(Cropped_Image_Location)




a = 1
for timePeriod_location in projectFolder:
    
    
    
    print(timePeriod_location)
    
    SAVE_Location = timePeriod_location + '/Processed_Cropped_Images/'
    
    if not os.path.exists(SAVE_Location): #check to see if save folder exists and creates it if not. creates above folder if not all ready created.
        os.makedirs(SAVE_Location)


    try:
        Cropped_Images_L2A_R10 = glob.glob(timePeriod_location + '/Cropped_Image_Bands/Level_2A_Data/R10m/*tiff') 
    
    
        band2 = GetBand(2, Cropped_Images_L2A_R10) #Get image bands 
        band3 = GetBand(3, Cropped_Images_L2A_R10)
        band4 = GetBand(4, Cropped_Images_L2A_R10)
        band8 = GetBand(8, Cropped_Images_L2A_R10)

        resolutionName = "L2A_R10"


    
        print('ok')
    
        TrueColourImg(SAVE_Location)
        FalseColourRedImg(SAVE_Location)
        NormalizedDifferenceVegetationIndex(SAVE_Location)
    
        a = a + 1
    except:
        pass

    try:    
        Cropped_Images_L2A_R20 = glob.glob(timePeriod_location + '/Cropped_Image_Bands/Level_2A_Data/R20m/*tiff')
    
        band2 = GetBand(2, Cropped_Images_L2A_R20) #Get image bands 
        band3 = GetBand(3, Cropped_Images_L2A_R20)
        band4 = GetBand(4, Cropped_Images_L2A_R20)
        band8 = GetBand(8, Cropped_Images_L2A_R20)

        resolutionName = "L2A_R20"

        TrueColourImg(SAVE_Location)
        FalseColourRedImg(SAVE_Location)
        NormalizedDifferenceVegetationIndex(SAVE_Location)
    
        a = a + 1
    except:
        pass

    try:
        Cropped_Images_L2A_R60 = glob.glob(timePeriod_location + '/Cropped_Image_Bands/Level_2A_Data/R60m/*tiff')
    
        band2 = GetBand(2, Cropped_Images_L2A_R60) #Get image bands 
        band3 = GetBand(3, Cropped_Images_L2A_R60)
        band4 = GetBand(4, Cropped_Images_L2A_R60)
        band8 = GetBand(8, Cropped_Images_L2A_R60)

        resolutionName = "L2A_R60"

        TrueColourImg(SAVE_Location)
        FalseColourRedImg(SAVE_Location)
        NormalizedDifferenceVegetationIndex(SAVE_Location)
    
    except:
        pass

    try:

        Cropped_Images_L1C = glob.glob(timePeriod_location + '/Cropped_Image_Bands/Level_1C_Data/*tiff')

        band2 = GetBand(2, Cropped_Images_L1C) #Get image bands 
        band3 = GetBand(3, Cropped_Images_L1C)
        band4 = GetBand(4, Cropped_Images_L1C)
        band8 = GetBand(8, Cropped_Images_L1C)



        TrueColourImg(SAVE_Location)
        FalseColourRedImg(SAVE_Location)
        NormalizedDifferenceVegetationIndex(SAVE_Location)

    except:
        pass
    print(Cropped_Images_L2A_R10)


    TrueColourImageLocation = timePeriod_location + '/True_Colour_Image' #location of folder to save images to 
    FalseColourImageLocation = timePeriod_location + '/False_Colour_Image'
    NDVIlocation = timePeriod_location + '/NDVI'
    
    
    print('ok')

    if not os.path.exists(SAVE_Location): #check to see if save folder exists and creates it if not. creates above folder if not all ready created.
        os.makedirs(SAVE_Location)


print("Complete")