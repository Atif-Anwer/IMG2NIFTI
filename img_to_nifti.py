"""
# -----------------------------------------------------------
# IMG to NIFTI Converter
#
# Uses Packages:
#     	- nibabel (https://nipy.org/nibabel/)
#     	- oct converter (https://github.com/marksgraham/OCT-Converter)
#     	- numpy (https://numpy.org/)
#
# -----------------------------------------------------------
"""

import argparse
import glob
import os

# import cv2
import nibabel as nib
import numpy as np
import PIL
import rerun as rr
from natsort import natsorted
from oct_converter.image_types import (FundusImageWithMetaData,
                                       OCTVolumeWithMetaData)
from oct_converter.readers import FDS, IMG, Dicom
from PIL import Image


# ---------------------------
def parse_args():
	"""
	Input arguments
	"""
	parser = argparse.ArgumentParser(description="Converting Carl Zeiss encoded IMG files to Nifti format.")

	desc = "Script to convert IMG files to NIFTI volumes"
	parser = argparse.ArgumentParser( description = desc )

	# Flags
	parser.add_argument( '--path', default = '/home/atif/Documents/Datasets/DICOM/testPath', help = 'Path to Folder containing Zeiss IMG files' )
	parser.add_argument( '--rows', type = int, default = 500, help = '(default=500) Image row dimension' )
	parser.add_argument( '--cols', type = int, default = 1536, help = '(default=1536) Image column dimension' )

	# parser.add_argument( '--preview', type = bool, default = True, help = '(default=False) Preview random 50 slices of the IMG file' )
	parser.add_argument( '--save_video', type = bool, default = False, help = '(default=False) Save the Zeiss IMG file as mp4 video' )
	parser.add_argument( '--save_slices', type = bool, default = False, help = '(default=False) Save the Zeiss IMG file as image slices' )
	# parser.add_argument( '--export_metadata', type = bool, default = False, help = '(default=False) Save the metadata as txt file' )

	args, unknown = parser.parse_known_args()

	return args

def main():
	"""
	Convert IMG files to NIFTI volumes
	"""

	# ---------------- PARSE ARGS ---------------- ::
	args = parse_args()
	if len( vars (args) ) < 1:
		# check minimum arguments provided
		print("No IMG file path provided => Type --help for aditional parameters ")
		exit(1)

	q = vars( args )
	print( '------------ Selected Options -------------' )
	for k, v in ( q.items() ):
		print( '%s: %s' % (str( k ), str( v )) )

	# ---------------- PROCESS IMG FILES ---------------- ::
	root_path = str(args.path) + "/*.img"
	print(root_path)

	for filepath in natsorted(glob.glob(root_path)):
		# Debug print file name
		print( '-------------- - ----------------' )
		print(f"[Info]: Processing video file: {filepath}")

		# filepath = args.path
		img = IMG(filepath)

		# get file name and current path.
		path, file = os.path.split(filepath)
		filename = os.path.splitext(file)[0]
		imgfolder = "{}/{}".format(path,filename)


		# returns an OCT volume with additional metadata if available
		oct_volume = img.read_oct_volume( rows= args.rows, cols=args.cols )
		num_slices = len(oct_volume.volume)
		print(f'[Info]: Detected Volume slices = {num_slices}')


		# ---------------- OPTIONAL STUFF ---------------- ::
		# Save volume as Mp4 video
		if args.save_video == True:
			video_filename = path+"/"+filename+"_"+str(num_slices)+".mp4"
			oct_volume.save(video_filename)
			print(f"[Info]: Saved MP4 Video.")

		# ---------------- CONVERT TO NIFTI ---------------- ::
		# This is the RAS convention for Neurological images (LAS is used by Radiological images)
		affine = np.eye(4)

		# Construct a new empty header - OPTIONAL ARG (patient and image information)
		empty_header = nib.Nifti1Header()
		empty_header.get_data_shape()

		# defining np array
		np_array = []

		# ---------------- PARSE THE FILE ---------------- ::
		# # Parse the img file for conversion. Save the slices if required
		for index, slice in enumerate(oct_volume.volume):
			np_array.append(slice)
			# Optional: Save volume slices as images
			if args.save_slices == True:
			# checking if the directory exist or not.
				if not os.path.exists(imgfolder):
					# if not present then create it.
					print(f"[info]: Creating folder {imgfolder}")
					os.makedirs(imgfolder)
				# save a slice in the folder (incrementing name)
				new_filename = "{}/{}_{}.png".format(imgfolder, filename, index)
				# cv2.imwrite(new_filename, cv2.rotate(slice, cv2.ROTATE_90_COUNTERCLOCKWISE))'
				im = Image.fromarray(slice)
				im = im.rotate(90, expand=True)
				im.save(new_filename)

		if args.save_slices == True and index > 0:
			print(f"[Info]: Saved {num_slices} image slices at {imgfolder}")

		# Convert to array
		np_array = np.array(np_array)

		# ---------------- SAVE TO NIFTI ---------------- ::
		nifti_file = nib.Nifti1Image(np_array, affine, empty_header)

		new_filename = path+"/"+"Converted_"+filename+".nii.gz"
		nib.save(nifti_file, new_filename)
		print(f"[Info]: Saved converted file {new_filename}.")

		print('--- File converted sucessfully. ---')

# ------------------------------------------------
if __name__ == "__main__":
    main()