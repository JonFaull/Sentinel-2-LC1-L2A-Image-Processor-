# Sentinel 2 LC1/L2A Image Processor
Program to create True/False Colour and NDVI Images from Sentinel 2 products

## Introduction:

This program was designed to work off the Sentinel 2 Automatic Downloader repo included here. It takes the generated cropped mosaics and creates True Colour Image, False Colour Image and a NDVI images for each of the sensing time frames. As is, this program will only work if you have run the previus Sentinel downloader code but the important sections of the code is in varios functions that can be reworked as desired. 

## Dependencies:

This program was written in Windows 10 using Python 3.6 anad an Anaconda installation. Python 3.6 can be downloaded [here](https://repo.continuum.io/archive/), I use `Anaconda3-5.2.0-Windows-x86_64.exe`. 

The following python packages are needed and can be install via `PIP`: `, matplotlib, numpy, glob, os, sys, gc, pygeoj, fnmatchm re`.

The following python package are also needed and can be downloaded [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/): `rasterio`.

Navigate in the terminal to your download location and you can `PIP` install them from there:
 `pip install rasterio-0.24.0-cp27-none-win32.whl`

## Getting Started:

Providing you have all the dependencies installed, running the program should be pretty straight forward and you should only need to change the following variables: 

`ProjectName = '2018-6-1 - 2018-7-10_Donegal_30_L2A'`
`projectFolder = 'E:/Products`   

The `ProjectName` is the name of the folder that was created by the Sentinel Downloader program and the `projectFolder` is the root directory where the project name is located. It should be the same as specified in the Sentinel Downloader program.

## Folder Structure: 

Once the program runs successfully, a `Processed_Cropped_Images`, will appear in the project folder. This will include the True Colour Images, False Colour Images and NDVI images. If you are working with L2A data it will create each file at the three 10m, 20, and 60m resolution. If you are working at LC1 it will create one of each at 10m resolution. 

   


