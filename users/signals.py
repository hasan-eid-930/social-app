from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect
from django.db.models.signals import post_save
from allauth.account.models import EmailAddress
from .models import Profile
from django.contrib.auth import get_user_model
from allauth.account.signals import email_confirmed
from django.urls import reverse


User=get_user_model()

@receiver(post_save, sender=User)  
def create_profile(sender, instance, created, **kwargs):
    # current instance of sender model
    user = instance
    # if newly created object
    if created:
        Profile.objects.create(
            user = user,
            email = user.email
        )
    # updated instance 
    else:
        profile = get_object_or_404(Profile, user=user)
        profile.email = user.email
        profile.save()
        
        
        
@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    profile = instance
    if created == False:
        user = get_object_or_404(User, id=profile.user.id)
        # chech if data is same ==> no need update
        # ==> prevent loop because user and profile 
        # send update each other
        if user.email != profile.email:
            user.email = profile.email
            user.save()

@receiver(post_save, sender=Profile)
def update_account_email(sender, instance, created, **kwargs):
    profile = instance
    if not created:
        try:
            email_address = EmailAddress.objects.get_primary(profile.user)
            if email_address.email != profile.email:
                email_address.email = profile.email
                email_address.verified = False
                email_address.save()
        except:
            pass


def redirect_to_onboarding(sender, request, email_address, **kwargs):
    # Redirect to onboarding page
    print('x')
    return redirect('profile-onboarding')

email_confirmed.connect(redirect_to_onboarding)