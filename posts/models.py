import uuid
from django.db import models
# import get_user-model()
from django.contrib.auth import get_user_model

# get current user model  
User=get_user_model()

class Post(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=500)
    # artist = models.CharField(max_length=500, null=True)
    # url = models.URLField(max_length=500, null=True) 
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='posts')
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name="likedposts", through="LikedPost")
    tags = models.ManyToManyField('Tag')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return f'/post/{self.id}'
        
class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.post.title}'
        
        
class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']

    def get_absolute_url(self):
        return f'/category/{self.slug}/'
        
        
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment=models.ForeignKey('Comment', on_delete=models.CASCADE,null=True, blank=True, related_name='replies')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable=False)

    def __str__(self):
        return f'{self.author.username} : {self.body[:30]}' 
        
    class Meta:
        ordering = ['-created']
        
        
class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.comment.body[:30]}'
