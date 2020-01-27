from django.db import models
from django.utils import timezone
from django.urls import reverse
from django import forms

# added for user registration
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    #author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    #title = models.CharField(max_length=200)
    Course = models.CharField(max_length=200)
    
    #added 1/26/2020

    When = models.CharField(max_length=200, blank=True, null=True)
    Instructor = models.CharField(max_length=200, blank=True, null=True)
    
    text = models.TextField()
    create_date=models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):

        self.published_date=timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        #eventually we will have post_detail html page!
        return reverse("post_detail",kwargs={'pk':self.pk})
    
    def __str__(self):
        return self.Course


class Comment(models.Model):
    post=models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment=True
        self.save()

    

    def get_absolute_url(self):
        #return list of blog post after user commented.
        return reverse('post_list')

    def __str__(self):
        return self.text

#added for user registration
class UserProfileInfo(models.Model):
    
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Add any additional attributes you want
    portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField(upload_to='basic_app/profile_pics',blank=True)
    
    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

