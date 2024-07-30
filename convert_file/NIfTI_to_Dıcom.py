import os
import nibabel as nib
import pydicom
from pydicom.dataset import Dataset, FileDataset
import numpy as np
import datetime
import time

def nifti_to_dicom(nifti_file, output_dir):
    # NIfTI dosyasını oku
    nifti_img = nib.load(nifti_file)
    nifti_data = nifti_img.get_fdata()
    
    # Çıkış dizinini oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # NIfTI verilerini dilimle ve her bir dilimi DICOM formatında kaydet
    for i in range(nifti_data.shape[2]):
        # DICOM dosyası için bir dataset oluştur
        dicom_dataset = Dataset()
        dicom_dataset.PatientName = "Test"
        dicom_dataset.PatientID = "123456"
        dicom_dataset.Modality = "MR"
        dicom_dataset.SeriesInstanceUID = "1.2.3"
        dicom_dataset.StudyInstanceUID = "4.5.6"
        dicom_dataset.FrameOfReferenceUID = "1.2.3.4.5.6"
        dicom_dataset.SOPInstanceUID = pydicom.uid.generate_uid()
        dicom_dataset.SOPClassUID = pydicom.uid.MRImageStorage
        dicom_dataset.ImagePositionPatient = [0, 0, i]
        dicom_dataset.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
        dicom_dataset.PixelSpacing = [1, 1]
        dicom_dataset.SliceThickness = 1
        dicom_dataset.Rows, dicom_dataset.Columns = nifti_data.shape[:2]
        dicom_dataset.InstanceNumber = i
        dicom_dataset.SamplesPerPixel = 1
        dicom_dataset.PhotometricInterpretation = "MONOCHROME2"
        dicom_dataset.BitsAllocated = 16
        dicom_dataset.BitsStored = 16
        dicom_dataset.HighBit = 15
        dicom_dataset.PixelRepresentation = 1
        dicom_dataset.PixelData = (nifti_data[:, :, i].astype(np.int16)).tobytes()
        
        # DICOM dosyasının kaydedileceği yolu oluştur
        dicom_file = os.path.join(output_dir, f"slice_{i:04d}.dcm")
        
        # DICOM dosyasını kaydet
        dicom_dataset.save_as(dicom_file)
        
    print(f"Conversion completed. DICOM files are saved in {output_dir}")

# Kullanım
nifti_file = "path/to/your/file.nii.gz"
output_dir = "path/to/output/directory"
nifti_to_dicom(nifti_file, output_dir)
