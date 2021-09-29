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

@login_required
def contacts(request):
    return render(request,'temps/contact.html')

def signup(request):
    name = "Sign Up"
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('username')
            send_an_mail(
            'Welcome to Neighbourhood App.',
            f'Hello {name},\n '
            'Welcome to Neighbourhood App and have fun.',
            'nyururukelvin99@gmail.com@gmail.com',
            [email],
            fail_silently=False,
            )
        return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form, 'name':name})

@login_required
def search_business(request):
    """
    Function that searches for projects
    """
    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_business = Business.objects.filter(name__icontains=search_term)
        message = f"{search_term}"
        businesses = Business.objects.all()
        
        return render(request, 'temps/search.html', {"message": message, "businesses": searched_business})

    else:
        message = "You haven't searched for any term"
        return render(request, 'temps/search.html', {"message": message})

@login_required
def edit_profile(request,username):
    current_user = request.user
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=current_user)
            form = UpdateProfile(request.POST,instance=profile)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = current_user
                profile.save()
            return redirect('index')
        except:
            form = UpdateProfile(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = current_user
                profile.save()
            return redirect('index')
    else:
        if Profile.objects.filter(user=current_user):
            profile = Profile.objects.get(user=current_user)
            form = UpdateProfile(instance=profile)
        else:
            form = UpdateProfile()
    return render(request,'temps/edit_profile.html',{"form":form})
@login_required
def post(request):

    current_user=request.user

    try:
        profile = Profile.objects.get(user = current_user)
    except:
        return redirect('edit_profile',username = current_user.username)

    try:
        posts = Post.objects.filter(neighbourhood = profile.neighbourhood)
    except:
        posts = None

    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=current_user
            post.neighbourhood = profile.neighbourhood
            post.save()
        return redirect('index')
    
    else:
        form=PostForm()
        
    return render(request,'temps/post.html',{'form':form, 'posts':posts})

@login_required
def business(request):
    current_user = request.user
    neighbourhood = Profile.objects.get(user = current_user).neighbourhood
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.neighbourhood = neighbourhood
            business.save()
            return redirect('business')
    else:
        form = BusinessForm()

    try:
        businesses = Business.objects.filter(neighbourhood = neighbourhood)
    except:
        businesses = None

    return render(request,'temps/business.html',{"businesses":businesses,"form":form})

class BusinessList(APIView):
    def get(self, request, format=None):
        all_businesses = Business.objects.all()
        serializers = BusinessSerializer(all_businesses, many=True)
        return Response(serializers.data)