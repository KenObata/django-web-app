from django.shortcuts import render,get_object_or_404,redirect


from blog.models import Post,Comment
from django.views.generic import (TemplateView,ListView,DetailView
                                  ,CreateView,UpdateView,DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm, CommentForm

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        #recent date comes first
        #      Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    # I don't want anyone have access to this CreateView
    login_url ='/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url ='/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


from django.urls import reverse_lazy
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url =reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        #if this is draft, there should be no publication date.
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


#############################################
from django.utils import timezone
#pk=primary key

#require login
@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)

    if request.method =='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            #don't want to commit yet. so...
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)

    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

#approve comment by admin
@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish
    return redirect('post_detail',pk=pk)

