from __future__ import division 
from PIL import Image
import os
from . import redis_handle
from . import db_handle
import imagehash 
from io import BytesIO
dir_path = os.path.dirname(os.path.realpath(__file__))
source_path = ''.join([dir_path,"/raw_images/"])

def stringSplit(string,length):
	return (string[0+i:length+i] for i in range(0,len(string),length))

def folderCreate(hash_of_image):
	folder_path=''.join([dir_path,"/image_source/"])
	for i in stringSplit(hash_of_image,2):
		folder_path=''.join([folder_path,i,"/"])
		try:
			os.makedirs(folder_path)
		except Exception as e:
			pass
	return folder_path

isValidImage=True

def cropper(image,filename):
		# Params
		width,height=image.size[0],image.size[1]
		cropStartX=0
		cropStartY=0
		cropEndX=0
		cropEndY=0
		cropHeight=height
		cropWidth=width
		# buff=BytesIO() do not remove.Useful for reference
	# Width adjustment
		if width<320:
			width=320
			image=image.resize((width,height))
	# Crop to keep the aspect ratio between 1.91:1 to 4:5
	#If aspect ratio less than 1.91:1
			# image.save(buff, 'JPEG', quality=100) do not remove.Useful for reference
		should_crop=False
		if height*1.91<width:
			should_crop=True
			cropWidth=height*1.91
			cropStartX=int((width/2)-(cropWidth/2))
			cropStartY=0
			cropEndX=int(cropStartX+cropWidth)
			cropEndY=height #Usually it's cropStartX+heightOfRequiredArea.Here cropStartX is 0 and we need full height.So..
		elif width*5<height*4:
			should_crop=True
			cropHeight=int((width*5)/4)
			cropStartX=0
			cropStartY=int((height/2)-(cropHeight/2))
			cropEndX=width #See comment of cropEndX
			cropEndY=int(cropStartY+cropHeight)
		if should_crop:
			print("[Information] Cropping file  "+filename)
			image=image.crop((cropStartX,cropStartY,cropEndX,cropEndY))
		return image

def resizer(image,filename):
		# If image is too big (rare case),resize it to 1080,1350 range, , without affecting aspect ratio
		width,height=image.size[0],image.size[1]
		if width>1080 or height>1350:
			print("[Warning] resizing "+filename+" since it's too big")
			new_width=width
			new_height=height
			if width>height:
				new_width=1080
				new_height=int(new_width/(width/height))
			elif height>width:
				new_height=1350
				new_width=int(new_height/(height/width))
			else:#If it's a big square image
				new_width=1080
				new_height=1080
			image=image.resize((new_width,new_height))
		return image
			# print(image.size[0])
			# All image processing is done above ^

def add_to_db_disk_redis(hash_of_image,image,full_image_path,tags):
	temp_bytes=BytesIO()
	image.save(temp_bytes,'JPEG',quality=50)
	isError=db_handle.add_to_db(hash_of_image,tags)
	if isError==None:
		image.save(full_image_path,'JPEG',quality=50)
		redis_handle.add_to_redis_feed(hash_of_image,temp_bytes.getvalue())
		return True,isError
	else:
		print("Error while DB")
		return False,isError

def aspectRatioResize(filename,raw_tags):
	isValidImage=True
	tags=raw_tags.split(',')
	print("tags",tags)
	# **Loading the image and Checking 1.whether the image is valid file,2.whether it's file (shouldn't be a folder )
	file_path=''.join([source_path,filename])
	try:
		image=Image.open(file_path)
	except Exception as e:
		print("[Failure] Corrupted file  "+filename)
		isValidImage=False
	if os.path.isfile(file_path)==False or isValidImage==False:
		print("[Failure] Skipping the file ",filename," because -->is_a_file=",os.path.isfile(file_path)," , -->is_valid_image=",isValidImage)
		return False #DND Affects upload_done.html
	image=cropper(image,filename)
	image=resizer(image,filename)
	hash_of_image=str(imagehash.dhash(image))
	full_image_path=''.join([folderCreate(hash_of_image),hash_of_image,".jpg"])
	image=image.convert('RGB')
	status,error= add_to_db_disk_redis(hash_of_image,image,full_image_path,tags)
	if(error!=None):
		print("[Fatal]",error)
	return status #DND Affects upload_done.html
