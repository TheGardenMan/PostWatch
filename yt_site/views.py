from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# . importing from this folder.In django,if modules are in same folder,simply importing doesn't work
from . import db_handle 
from . import redis_handle
from . import image_handle
from .forms import tags_image_form
'''
	image_handle does both tags and image
'''
def upload_file(request):
	# if file uploaded,below if statement will be true
	# https://www.javatpoint.com/django-file-upload
	if request.method == 'POST' and request.FILES['raw_image']:
		form_data=tags_image_form(request.POST,request.FILES)
		# Once is_valid is done,data is available in form_data.cleaned_data
		if form_data.is_valid():
			raw_image = request.FILES['raw_image']
			filename=raw_image.name
			# if filename already there,name will be changed.To get original file name from disk,see handle_uploaded_image func.
			raw_tags=form_data.cleaned_data['tags']
			print(raw_tags)
			upload_status=handle_uploaded_image(raw_image,raw_tags)
			return render(request, 'upload_done.html', {'filename': filename,'upload_status':upload_status})
	tags_image_form_=tags_image_form()
	return render(request, 'upload_file.html',{'tags_image_form_':tags_image_form_})


def handle_uploaded_image(raw_image_uploaded,raw_tags):
	print("handling ",raw_image_uploaded.name)
	fs = FileSystemStorage()
	file_name_in_disk=fs.save(raw_image_uploaded.name, raw_image_uploaded)
	return image_handle.aspectRatioResize(raw_image_uploaded.name,raw_tags)

def home(request,page_number=None):
	if page_number==None:
		content={'page_number':'1'}
		return render(request,'index.html',content)
	else:
		hashes_and_tags=[]
		hashes_and_tags=db_handle.get_n_image_hashes_and_tags(page_number)
		page_number=int(page_number)+1
		hashes_len=len(hashes_and_tags)
		if(hashes_len==0):
			return render(request,"not_found.html")
		elif (hashes_len<10 and hashes_len>0):
			page_number=0#Preventing next page link from being shown
		content={'page_number':page_number,'hashes_and_tags':hashes_and_tags}
		return render(request,'images.html',content)

def search(request):
	print(request)

def image_serve(request,hash_of_image):
	image_data=redis_handle.get_from_redis_feed(hash_of_image)
	if image_data==None:
		print(hash_of_image+"not found")
		return HttpResponse(image_data, content_type="image/png")
	else:
		return HttpResponse(image_data, content_type="image/png")
