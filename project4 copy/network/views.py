import json
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect ,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from network.forms import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


from .models import *

def Pagignate_it(request ,obj):
    paginator = Paginator(obj, 10) # Show 25 contacts per page.
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return page_obj





def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def AddPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            # file is saved
            date = datetime.now
            new_post = Post(text=text,text_date=date, Texter= request.user)
            new_post.save()
            # creating the likes model
            l = liked(liked_post=new_post)
            l.save()
        
        return HttpResponseRedirect(reverse("index"))
       
    else:
        form = PostForm()
        return HttpResponseRedirect(reverse("index"))
        

    
def index(request):
    try:
        f = Follow_database(Person=request.user)
        f.save()
    except:
        pass
    Posted = Post.objects.all().order_by('text_date')[::-1]
    form = PostForm()
    paginator = Paginator(Posted, 10) # Show 25 contacts per page.
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render( request , "network/index.html" , {"Posts" :Posted ,"Form": form ,"page_obj": page_obj})
    return JsonResponse('hahaha', safe=False)


 

#Displaying the users profile and posts   
def User_Profile(request ,texter):
    User_Profile_info = User.objects.get(id=texter)
    Users_Posts = Post.objects.filter(Texter=User_Profile_info.id).order_by('text_date')[::-1]
    paginator = Paginator(Users_Posts, 4) # Show 25 contacts per page.
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    Follow_info = Follow_database.objects.get(Person=texter)  
    is_following = Follow_info.Followers.all()
    
    
    if request.user.id == int(texter):
        button = None

    elif  request.user in is_following:
        button = 'Unfollow'
       
    else:
        button = 'Follow'      
    return render( request , "network/Profile.html" , {"Posts" :Users_Posts ,"Profile": User_Profile_info ,"page_obj": page_obj ,"Button":button })    


#following and unfollowing other user
def Following(request, action, ID):
    #get the required users 
    target_person = User.objects.get(id=ID)
    profile_person_follow_data = Follow_database.objects.get(Person=target_person)

    current_user_follow_data = Follow_database.objects.get(Person=request.user)
    

    if action == 'Unfollow': #Unfollow
        profile_person_follow_data.Followers.remove(request.user)
        current_user_follow_data.Following.remove(target_person)
        
    elif action == 'Follow':      
        profile_person_follow_data.Followers.add(request.user)
        current_user_follow_data.Following.add(target_person)
    
    return HttpResponseRedirect(reverse("User_Profile",args=[ID]))
    


#Seeing posts from people that the user follows
@login_required
def Followed_people(request):
    followed_posts = []
    data = Follow_database.objects.get(Person=request.user)
    people_following = data.Following.all()
    
    #Get all the posts from people the user follows and add toan array
    for Person in people_following:
        persons_posts = Post.objects.filter(Texter=Person)
        for indie_post in persons_posts:
            followed_posts.append(indie_post)
        
    # pagigating the posts
    paginator = Paginator(followed_posts, 2) # Show 25 contacts per page.
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render( request , "network/following.html" ,{"Posts":followed_posts ,"page_obj": page_obj})


@csrf_exempt
@login_required   
def liked_posts(request , ID):

    if request.method == "GET":
        all_liked_posts = liked.objects.all()
        #Create a dictionary with only necessary information
        post_info = []
        
        for i in all_liked_posts:
            # Check if the current user liked that post
            if request.user in i.who_liked.all():
                user_liked = True
            else:
                user_liked =  False
            
            post_writer = i.liked_post.Texter
             
            # if the post belongs to the logged on user it should be changeable else not
            if post_writer == request.user:
                changeable = True
            else:
                changeable = False

            dicti = {"id" : i.liked_post.id , "likes": i.likes , "user_like":user_liked , "Edit":changeable}
            post_info.append(dicti)
       

        return JsonResponse(post_info , safe=False)


# adding likes and removing likes
@csrf_exempt
def like_or_unlike(request ,ID):
    #Query requestested post
    try:
        post = Post.objects.get(id=ID)
    except :
        print("Try failed")
        return JsonResponse({"error":"Post not Found"} , status=404)

    if request.method == "POST":
        data = json.loads(request.body)
        print(data) 
    
    the_user = User.objects.get(id=data["user"])
    
    # Unliking by removing some data from the database
    if data["liked"] == True:
        post_liked = liked.objects.get(liked_post=post)
        post_liked.who_liked.remove(the_user)
        post_liked.likes = post_liked.who_liked.all().count()
        post_liked.save()
    #Adding likes 
    else:
        post_liked = liked.objects.get(liked_post=post)
        post_liked.who_liked.add(the_user)
        post_liked.likes = post_liked.who_liked.all().count()
        post_liked.save()
      
# Posts that belong to the user which they can edit
@csrf_exempt
def Edit_post(request):
    # Changing the post 

    all_posts = Post.objects.all()
    Edit_info = []

    for i in all_posts:
        post_writer = i.Texter

        if post_writer == request.user:
            changeable = True
        else:
            changeable = False
        
        dicti = {"Post_id" : i.id , "Edit":changeable}
        Edit_info.append(dicti)
        
    print(Edit_info) #testing output

    return JsonResponse(Edit_info , safe=False)


#Editing posts using JSON
@csrf_exempt
def Edit(request , ID):
    # Check if post exitsts 
    try:
         Current_post = Post.objects.get(id=ID)
    except: 
        pass
    
    if request.method == "PUT":
        data = json.loads(request.body)
       
        if data.get("text") is not None:
            Current_post.text = data["text"]
        Current_post.save()
        return HttpResponse(status=204)

    # Pmail must be via PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

 