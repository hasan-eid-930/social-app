from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *


@login_required 
def home(request):
    posts=Post.objects.all()
    context={'posts':posts}
    return render(request,'posts/home.html',context)

def post_page(request,pk):
    post = get_object_or_404(Post, id=pk)
    context={'post':post}
    return render(request,'posts/post_page.html',context)

@login_required
def post_create(request):
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST,request.FILES)
        if form.is_valid():
            # returm model instance without saving it to db
            post = form.save(commit=False)
            
            post.author = request.user
            
            post.save()
            # used if commit= false and form's model contain m2m field 
            form.save_m2m()
            return redirect('home')
    
    return render(request, 'posts/post_create.html', {'form' : form })

@login_required
def post_delete(request, pk):
    # i specify author to make sure i am post's owner
    
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post deleted successly')
        return redirect('home')
        
    return render(request, 'posts/post_delete.html', {'post' : post})


def post_edit(request,pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    form = PostEditForm(instance=post)
    if request.method == 'POST':
        form = PostEditForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully')
            
            return redirect('home')  
    context={"post":post,
             "form":form}
    return render(request, 'posts/post_edit.html', context)