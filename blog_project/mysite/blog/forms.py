from django import forms
from blog.models import Post, Comment
#from blog.models import UserProfileInfo

#added for user registration
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta():
        year_choice=['Before 2016',
                     '2016 Fall','2016 Summer','2016 Spring',
                     '2017 Fall','2017 Summer','2017 Spring',
                     '2018 Fall','2018 Summer','2018 Spring',
                     '2019 Fall','2019 Summer','2019 Spring',
                     '2020 Spring',
                     ]
        model = Post
        #fields = ('author','title','text') #deleted author
        fields = ('Course','When','Instructor','text')

        widgets = {
            #our class = textinputclass,postcontent
            'Course':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
            #'When':forms.Select(choices=year_choice)
            }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Post
        #fields = ('author','text') deleted author
        fields = ('text',)

        widgets = {
            #our class = textinputclass,postcontent
            #'author':forms.TextInput(attrs={'class':'textinputclass'}),
            #default
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
    
        }

########### added for user registration ######################
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta():
        model = User
        fields = ('username','email','password')

"""
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')
"""
