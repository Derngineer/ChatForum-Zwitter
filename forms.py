from django import forms
from django.contrib.auth.models import User
from .models import Zweet,Reply

class ZweetForm(forms.ModelForm):
	body = forms.CharField(max_length=200, widget=forms.Textarea)

	class Meta:
		model = Zweet
		fields =('body',)
		
class ReplyForm(forms.ModelForm):
	text = forms.CharField(max_length=200, widget = forms.Textarea)
	class Meta:
		model = Reply
		fields = ('text',)