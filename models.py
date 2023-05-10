from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.

class Zweet(models.Model):
	user =models.ForeignKey(
		User, related_name ='zweets',
		on_delete = models.DO_NOTHING
		)

	body =  models.CharField(max_length = 200)
	created_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return (
			f'{self.user}'
			f'({self.created_at: %Y-%m-%d %H:%M})'
			f'{self.body}'
			)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	follows = models.ManyToManyField('self',
		related_name ='followed_by',
		symmetrical = False,
		blank = True
		)
	date_modified = models.DateTimeField(User,auto_now = True)
	def __str__(self):

		return self.user.username


	# Create profile when new user signs up

def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()
		user_profile.follows.set([instance.profile.id])

post_save.connect(create_profile,sender = User)


class Reply(models.Model):
	parent = models.ForeignKey('self',null = True, blank=True, on_delete = models.CASCADE, related_name ='replies')
	zweet = models.ForeignKey(Zweet, on_delete = models.CASCADE,related_name = 'replies')
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	text = models.CharField(max_length = 200)
	created_at = models.DateTimeField(auto_now_add = True)

	@property
	def children(self):
		return Reply.objects.filter(parent = self).order_by('-created_at').all()

	@property
	def is_parent(self):
		if self.parent is None:
			return True
		return False
	


	def __str__(self):
		return (
			f'{self.user}'
			f'({self.created_at: %Y-%m-%d %H:%M})'
			f'{self.text}'
			)
