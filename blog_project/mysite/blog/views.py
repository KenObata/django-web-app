from django.shortcuts import render,get_object_or_404,redirect


from blog.models import Post,Comment
from django.views.generic import (TemplateView,ListView,DetailView
                                  ,CreateView,UpdateView,DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm, CommentForm

# for user registration
from blog.forms import UserForm #UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
class AboutView(TemplateView):
    template_name = 'blog/about.html'


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
    form_class = PostForm # from .forms import PostForm
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
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post

    def get_queryset(self):
        #if this is draft, there should be no publication date.
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


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
    post.publish()
    return redirect('post_detail',pk=pk)

############################################
# user registration
def register(request):
    
    registered = False
    
    if request.method == 'POST':
        
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        #profile_form = UserProfileInfoForm(data=request.POST)
        
        # Check to see both forms are valid
        if user_form.is_valid():
            
            # Save User Form to Database
            user = user_form.save()
            
            # Hash the password
            user.set_password(user.password)
            
            # Update with Hashed password
            user.save()
            """
            # Now we deal with the extra info!
            
            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)
            
            
            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user
            
            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']
            """
            # Now save model
            #profile.save()
    
            # Registration Successful!
            registered = True
        
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
#profile_form = UserProfileInfoForm()
    
    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'blog/registration.html',
                  {'user_form':user_form,
                  #'profile_form':profile_form,
                  'registered':registered})

# user login view
def user_login(request):
    
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)
        
        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                #return HttpResponseRedirect(reverse('index'))
                return HttpResponseRedirect(reverse('post_list'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'blog/user_login.html', {})
