#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:06:29 2020

@author: wangmeiqi
"""


import os
import SimpleITK as sitk

#route = your dicom folder

route = '/Volumes/dataBackup/HCC/ntuh/non_labeled/CT_orginal_six_examples'

#save_route = the folder where you want to save your output files

save_route = '/Volumes/dataBackup/HCC/ntuh/non_labeled' #/CT_3D_10282020

slice_list = []

dir_ = []


dir_ = os.listdir(route)

num1 = len(dir_)

        
for i4 in range(len(dir_)):
    
    file = dir_[i4]
    
    print(str(i4+1) + '/' + str(num1))
    
    print(file)
    
    dicomPath = os.path.join(route, file)
    
    reader = sitk.ImageSeriesReader()

    series_ids = reader.GetGDCMSeriesIDs(dicomPath)

    for i in range(len(series_ids)): #series
    
        series_id = series_ids[i]
    
        dicom_filenames = reader.GetGDCMSeriesFileNames(dicomPath, series_id)
    
        if len(dicom_filenames)>10:
        
            print(series_id)
        
            sitkReader = sitk.ImageFileReader()
        
            #找有幾種acquisition number
            max_acquisition = 1
        
            for i1 in range(len(dicom_filenames)):
            
                fileReader = sitk.ImageFileReader()
            
                fileReader.SetFileName(dicom_filenames[i1])

                fileImage = fileReader.Execute()
                
                #print(dicom_filenames[i1])
                
            if fileImage.GetMetaData("0020|0012") == '':
                
                # 設定 DICOM 影像序列檔案名稱
                reader.SetFileNames(dicom_filenames)
            
                # 載入後設資料
                reader.MetaDataDictionaryArrayUpdateOn()
         
                # 載入私有後設資料
                reader.LoadPrivateTagsOn()
                
                image = reader.Execute()
                
                size = image.GetSize()
                
                print("Image size: {} x {} x {}".format(size[0], size[1], size[2]))
                
                save_path = os.path.join(save_route, file)
                
                if not os.path.isdir(save_path):
                        
                    os.mkdir(save_path)
                    
                outFile = os.path.join(save_path, series_ids[i] + ".nii.gz") # xxx.nii.gz
                
                sitk.WriteImage(image, outFile)
                    
                continue
                    
            else:
            
                acquisition = int(fileImage.GetMetaData("0020|0012"))
            
                if acquisition > max_acquisition:
                
                    max_acquisition = acquisition
                
                #print(str(max_acquisition))
                
                for i3 in range(1, max_acquisition + 1): #1~3
                
                    for i2 in range(len(dicom_filenames)):      
                
                        fileReader = sitk.ImageFileReader()
            
                        fileReader.SetFileName(dicom_filenames[i2])

                        fileImage = fileReader.Execute()
                
                        acquisition = int(fileImage.GetMetaData("0020|0012"))
                
                        if acquisition == i3:
                    
                            slice_list.append(dicom_filenames[i2])
                    
                
                    try:
                
                        print(len(slice_list))
                    
                        # 設定 DICOM 影像序列檔案名稱
                        reader.SetFileNames(slice_list)
                    
                        # 載入後設資料
                        reader.MetaDataDictionaryArrayUpdateOn()
                    
                        # 載入私有後設資料
                        reader.LoadPrivateTagsOn()
                    
                        image = reader.Execute()
                    
                        size = image.GetSize()
                    
                        print("Image size: {} x {} x {}".format(size[0], size[1], size[2]))
                    
                        save_path = os.path.join(save_route, file)
                    
                        if not os.path.isdir(save_path):
                        
                            os.mkdir(save_path)
                
                        outFile = os.path.join(save_path, series_ids[i] + "_acq_" + str(i3) + ".nii.gz") # xxx.nii.gz
                
                        sitk.WriteImage(image, outFile)
                    
                    except Exception as e: 
            
                        print(f'An Error occurred: {e}')
                
                    slice_list = []
