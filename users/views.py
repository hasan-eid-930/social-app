from django.contrib import messages
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from inbox.form import MessageCreateForm
from posts.forms import CommentCreateForm
from posts.models import Post
from .forms import *
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

User=get_user_model()






def profile(request,username=None):
    # i use request.user when information 
    # related to  current user
    if username:
        user=get_object_or_404(User,username=username)
    else:
        user=request.user
    try:
        profile=user.profile
    except:
        # return 404 exception
        raise Http404("Profile does not exist") 
    if request.htmx:

        if "top_comments" in request.GET:
            comments=user.comments.annotate(num_likes=Count("likes")).order_by('-num_likes')
            form=CommentCreateForm()       
            return render(request,'posts/partials/top_comments.html',{'comments':comments,'form':form})
        else:
            if 'top_posts' in request.GET:
                posts=user.posts.annotate(num_likes=Count("likes")).order_by('-num_likes')
            elif 'liked_posts':
                posts=user.likedposts.order_by('-likedpost__created')
            else:
                posts=user.posts.all()
            return render(request,'posts/partials/top_posts.html',{'posts':posts})
    form=MessageCreateForm()
    context={'profile':profile,'form':form}
    return  render(request,'users/profile.html',context)

@login_required
def profile_edit(request:HttpRequest):
    try:
        profile=request.user.profile
    except:
    # return 404 exception
        raise Http404("Profile does not exist")   
    form=ProfileEditForm(instance=profile)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            
            return redirect('profile')
    if request.path == reverse("profile-onboarding"):
        template= 'users/profile_onboarding.html' 
    else:
        template='users/profile_edit.html'
    context={"form":form}
    return render(request, template, context)

@login_required
def profile_delete(request):
    # i get user because when it logout 
    # ==> will be not exist on request
    user = request.user
    
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')
    
    return render(request, 'users/profile_delete.html' )

 