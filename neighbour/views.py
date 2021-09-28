from django.shortcuts import render,get_object_or_404,redirect,redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Post,Business,Profile,Neighbourhood,Comment
from .forms import PostForm,UpdateUser,SignUpForm,CommentForm,UpdateProfile,BusinessForm
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializer import BusinessSerializer
from .email import send_an_email


# Create your views here.
@login_required
def index(request):
    # Default view
    comments = Comment.get_comments()
    current_user = request.user
    try:
        profile = Profile.objects.get(user = current_user)
    except:
        return redirect('edit_profile',username = current_user.username)

    try:
        posts = Post.objects.filter(neighbourhood = profile.neighbourhood)
    except:
        posts = None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.post = Post.objects.get(id=int(request.POST["post_id"]))
            comment.save()
            return redirect('index')
    else:
        form = CommentForm()

    return render(request, 'temps/index.html', {'profile':profile,'posts': posts, 'form':form,'comments':comments})

def about(request):
    return render(request, 'temps/about_us.html')
