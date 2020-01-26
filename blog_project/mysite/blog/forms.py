from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author','title','text')

        widgets = {
            #our class = textinputclass,postcontent
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})

            }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author','text')

        widgets = {
            #our class = textinputclass,postcontent
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            #default
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
    
        }
