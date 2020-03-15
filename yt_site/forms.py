from django import forms

class tags_image_form(forms.Form):
	# If you don't give label,var name with 1st letter caps  becomes label.
	# Eg tags==> "Tags:" with a colon in the end
	tags = forms.CharField(max_length=100)
	raw_image = forms.FileField(label='Select Image')