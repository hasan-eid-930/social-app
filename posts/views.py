from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from posts.decorators import like_toggle
from django.core.paginator import Paginator
from .forms import *


def home(request,tag=None):
    if tag :
        posts=Post.objects.filter(tags__slug=tag)
        tag=get_object_or_404(Tag,slug=tag)
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 3)  # Show 3 posts per page.

    page_number = request.GET.get("page",1)
    posts = paginator.get_page(page_number)
    context={
        'posts':posts,
        'tag':tag
        }
    if request.htmx:
        return render(request,'posts/partials/posts_page_part.html',context)
    return render(request,'posts/home.html',context)

def post_page(request,pk):
    post = get_object_or_404(Post, id=pk)
    form=CommentCreateForm()
    if request.htmx:
        if 'top' in request.GET:
            comments=post.comments.annotate(num_likes=Count("likes")).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments=post.comments.all()
        context={'comments':comments,
                'form':form}
        return render(request,'posts/partials/loop_comments.html',context)
    
    
    context={'post':post,
             'form':form}
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

@login_required
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

@login_required
def comment_create(request,post_pk,comment_pk=None):
    post=get_object_or_404(Post,pk=post_pk)
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            # returm model instance without saving it to db
            comment = form.save(commit=False)
            
            comment.author = request.user
            comment.parent_post=post
            if comment_pk:
                parent_comment=get_object_or_404(Comment,pk=comment_pk)
                comment.parent_comment=parent_comment

            comment.save()
            # used if commit= false and form's model contain m2m field 
            form.save_m2m()
            context={'form':CommentCreateForm(),
                     'comment':comment,
                     'post':post
                     }
            return render(request,'posts/partials/comment_part.html',context)
    return redirect('post',post.id)
@login_required
def comment_delete(request, pk):
    # i specify author to make sure i am post's owner
    
    comment = get_object_or_404(Comment, id=pk, author=request.user)
    if request.method == "POST":
        comment.delete()
        messages.success(request, 'comment deleted successly')
        return redirect('post',comment.parent_post.id)
        
    return render(request, 'posts/comment_delete.html', {'comment' : comment})

# here pk is recived by decorator's wrapper
@login_required
@like_toggle(model_class=Post)
def post_like(request,post):
    return render(request,'posts/partials/likes.html',{'model':post})

@login_required
@like_toggle(model_class=Comment)
def comment_like(request,comment):
    return render(request,'posts/partials/likes.html',{'model':comment})


