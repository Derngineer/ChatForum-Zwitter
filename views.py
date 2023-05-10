from django.shortcuts import render,redirect
from .models import Profile,Zweet, Reply
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ZweetForm, ReplyForm
from django.shortcuts import get_object_or_404
from django.utils import timezone



# Create your views here.

def registration(request):

	if request.method == 'POST':
		form =UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('sign_in')
		else:
			print('form is not valid')
	else:
		print('method is not READ')
		form = UserCreationForm()
	return render(request,'zweets/registration.html',{'form':form})


def sign_in(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request,username = username, password = password)

		if user is not None:
			login(request,user)
			return redirect('home')

		else:
			messages.success(request,('was an error trying to sign'))

	return render(request,'zweets/sign_in.html',{})

def home(request):
	if request.user.is_authenticated:
		zweets = Zweet.objects.all().order_by('-created_at')
		replies = Reply.objects.all()
		return render(request, 'zweets/home.html',{'zweets': zweets, 'replies':replies})
	else:

		return render(request, 'zweets/home.html',{})




def profile_list(request):
	if request.user.is_authenticated:

		profiles = Profile.objects.exclude(user = request.user)
		return render(request,"zweets/profile_list.html",{'profiles': profiles })

	else:
		messages.success(request, ('You Must Be Logged In'))
		return render(request,'zweets/home.html',{})

def profile(request,pk):

	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id = pk)

		
		new_zweet = None
		parent_reply = None
		replies_reply = None 

		

		if request.method == 'POST':
			print('body' in request.POST)
			if 'body' in request.POST:
				zweet_form = ZweetForm(request.POST)
				print(zweet_form.errors)

				if zweet_form.is_valid():

					new_zweet =zweet_form.save(commit = False)
					new_zweet.user = request.user
					new_zweet.save()
					print('form saved')
					return redirect(request.path)


				else:
					print(zweet_form.errors)
			elif 'text' in request.POST:
				reply_form = ReplyForm(request.POST)
				if reply_form.is_valid():
					try:
						print('going through this')
						
						print('is it going past here!')
						parent_reply_id = request.POST.get('parent_reply_id',None)
						zweet = Zweet.objects.get(id=request.POST['zweet_id'])
						if parent_reply_id:
							print('this means reply id is there')
							parent_reply = Reply.objects.get(id =parent_reply_id)
						
						else:
							parent_reply = None
						new_reply = reply_form.save(commit = False)
						new_reply.user = request.user
						new_reply.zweet = zweet
						new_reply.parent = parent_reply
						new_reply.created_at = timezone.now()
						new_reply.save()
						messages.success(request, 'Reply Posted Successfully!')
						return redirect(request.path)
					except KeyError:
				
						messages.error(request, 'Something is wrong with your reply')
						print(reply_form.errors,'are there errors')

				else:
					print("here are the errors",reply_form.errors)

			elif 'follow' in request.POST:
				current_user_profile = request.user.profile
				action = request.POST['follow']
				if action == 'unfollow':
					current_user_profile.follows.remove(profile)
					messages.success(request, 'You have unfollowed this user')
				elif action == 'follow':
					current_user_profile.follows.add(profile)
					messages.success(request, 'You have followed this user')
					
		print('exited algorithm')

		print(type(request.user.id), type(pk))

		zweet_form = None
		# show_zweet_form = False
		if request.user.id == pk:
			print('FORM LOADED')
			zweet_form = ZweetForm()

		reply_form = ReplyForm()
			

			
		zweets = Zweet.objects.filter(user_id = pk).order_by('-created_at')
		replies = []
		for zweet in zweets:
			replies.extend(Reply.objects.filter(zweet = zweet))
	
		return render(request,'zweets/profile.html',{'profile':profile, "zweets" : zweets, 'zweet_form':zweet_form, 'replies':replies, 'reply_form':reply_form,})

	else:
		messages.success(request,('You must be logged in'))
		return render(request,'zweets/home.html',{})




