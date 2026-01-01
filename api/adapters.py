from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.utils.text import slugify

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

	def populate_user(self, request, sociallogin, data):
		user = super().populate_user(request, sociallogin, data)


		#Generate username from email
		email = data.get("email", "")
		user.username = slugify(email.split("@")[0])

		user.first_name = data.get("given_name", "")
		user.last_name = data.get("family_name", "")
		user.is_verified = True

		return user