from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, AddPosts, DetailForm
from .models import Detail, Post, Message, Room, Comments
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout


def home(request):
    try:
        user = Detail.objects.get(user=request.user)
        if(user.bool_abuse == True or user.bool_hate == True):
            return render(request, 'src_code/warning_page.html')
        else:
            posts = Post.objects.all()
        
            context = {
                'posts':posts,
            }
        return render(request, 'src_code/home.html', context)
    except:

        print("Hellloooo ...", request.user, request.user.username)
        posts = Post.objects.all()
        
        context = {
            'posts':posts,
        }
        return render(request, 'src_code/home.html', context)



def follow_unfollow(request, id_user, value):
    main_user = Detail.objects.get(user=request.user)
    add_following = Detail.objects.get(user__id=id_user)
    
    if value == '1':
        main_user.following.add(add_following.user)
        add_following.followers.add(main_user.user)

    if value == '0':
        main_user.following.remove(add_following.user)
        add_following.followers.remove(main_user.user)

    return redirect('user-page', id_user)


def message(request, receiver):
    sender = request.user
    receiver = User.objects.get(username=receiver)
    context = {
        'receiver_obj':receiver,
    }

    return render(request, 'src_code/message.html', context)



def send(request):
    # return render(request, 'src_code/home.html')
    print("I am here")
    if request.method == 'POST':

        sender = request.user
        receiver = request.POST['username']
        receiver = User.objects.get(username=receiver)
        name1 = str(str(sender) + str(receiver))
        name2 = str(str(receiver) + str(sender))
        if Room.objects.filter(room_name=name1).exists():
            room = Room.objects.get(room_name=name1)

        elif Room.objects.filter(room_name=name2).exists():
            room = Room.objects.get(room_name=name2)

        else:
            room = Room.objects.create(room_name=name1)


        message = request.POST['message']

        # hate_message = 1
        # abusive_message = 
        message_intention = check_message_intention(message)
        print(message)

        if message_intention == 'abusive_speech':
            print("Its abusive message")
            u = Detail.objects.get(user=request.user)
            u.bool_abuse = True
            u.save()
            logout(request)

            # return JsonResponse({'speech':message})
        elif message_intention == 'hate_speech':
            print("Its hate speech")
            u = Detail.objects.get(user=request.user)
            u.bool_hate = True
            u.save()
            logout(request)
            
            redirect('logout-page')
            print("i went to logout page")
            
        else:
            new_message = Message.objects.create(message=message, sender=sender, receiver=receiver)
            room.message.add(new_message)
            print("You are good to go")
        return HttpResponse("help")
        # return render(request, 'src_code/home.html')



def getMessages(request, receiver):
    # rcvUser = Detail.objects.get(user=receiver)
    # if rcvUser.bool_abuse == True or rcvUser.bool_hate == True:

    sender = request.user
    receiver = User.objects.get(username=receiver)
    name1 = str(str(sender) + str(receiver))
    name2 = str(str(receiver) + str(sender))
    u = Detail.objects.get(user=request.user)
    # if u.bool_hate == True:
    #     redirect('logout-page')
    
    if Room.objects.filter(room_name=name1).exists():
        room = Room.objects.get(room_name=name1)

    elif Room.objects.filter(room_name=name2).exists():
        room = Room.objects.get(room_name=name2)

    else:
        room = Room.objects.create(room_name=name1)
    try:
        messages = Room.objects.get(room_name=name1).message.all()
        return JsonResponse({"messages":list(messages.values())})
    except:
        messages = Room.objects.get(room_name=name2).message.all()
        return JsonResponse({"messages":list(messages.values())})


def individualPost(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comments.objects.filter(post_id=post.id)
    user = Detail.objects.get(user=request.user)

    context = {
        'post':post,
        'comments':comments,
        'user':user,
    }
    
    return render(request, 'src_code/individual_post.html', context)

def comment(request):
    user_who_comment_id = request.POST['user_who_commented']
    comment = request.POST['comment']
    post_id = request.POST['post']
    post = Post.objects.get(pk=post_id)

    user = User.objects.get(id=user_who_comment_id)
    cmt = Comments.objects.create(user=user, comment=comment, post=post)
    cmt.save()
    return redirect('individual-post-page', post_id)

def savedPost(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        if request.user in post.saved.all():
            post.saved.remove(request.user)
        else:
            post.saved.add(request.user)
    # return JsonResponse({"post":post,})
    return redirect('home-page')


def followers(request, pk_of_users, detail_of_user):
    d = {}
    user_is = User.objects.get(id=detail_of_user)
    detail = Detail.objects.get(pk=pk_of_users)
    for item in detail.followers.all():
        user = Detail.objects.get(user=item)
        d[user] = item
    
  
    context = {
        'detail':detail,
        'd':d.items(),
    }
    return render(request, 'src_code/followers.html', context)


def following(request, pk_of_users, detail_of_user):
    d = {}
    user_is = User.objects.get(id=detail_of_user)
    detail = Detail.objects.get(pk=pk_of_users)
    for item in detail.following.all():
        user = Detail.objects.get(user=item)
        d[user] = item
    
  
    context = {
        'detail':detail,
        'd':d.items(),
    }

    return render(request, 'src_code/following.html', context)

def userPage(request, user_id):
    
    try:
        user = Detail.objects.get(user__id=user_id)
        # if request.user.id != user_id and (user.bool_abuse == True or user.bool_hate == True):
        #     return render(request, 'src_code/blocked_user.html')
    except:

        user = Detail.objects.create(user=request.user, name='Hello World')

    print(user)
    if request.user.id != user_id and (user.bool_abuse == True or user.bool_hate == True):
        context = {
            'user':user,
        }
        print(context)
        return render(request, 'src_code/blocked_user.html', context)
    user_post = User.objects.get(pk=user_id)
    tag_posts = Post.objects.filter(tag=user_id)
    print('tag posts', tag_posts)
    posts = Post.objects.filter(user=user_post)
    main_user = Detail.objects.get(user=request.user)
 
    context = {
        'user':user,
        'posts':posts,
        'main_user':main_user,
        'tags':tag_posts,
    }
    currUser = Detail.objects.get(user=request.user)
    if currUser.bool_hate == True or currUser.bool_abuse == True:
        print("I am here")
        return render(request, 'src_code/warning_page.html')
    return render(request, 'src_code/user_page.html', context)

# def likes(request):
#     if request.method == 'POST':
#         print("I have reached here . Flag 1 ...........")
#         post_like_pk = request.POST['post_id']
#         post = Post.objects.get(pk=post_like_pk)
#         print("I have reached here . Flag 2 ...........")

#         if request.user in post.likes.all():
#             post.likes.remove(request.user)
#             return JsonResponse({"result":1, })

#         else:
#             post.likes.add(request.user)
#             return JsonResponse({"result":2, })
        # return HttpResponse("Message send successfullly")

        # return redirect('home-page')


def likes(request):
   

    user = request.user
    print("Hiii")
    if request.method == 'POST':
        print("hello")
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
            print("removed the user")
        else:
            post_obj.likes.add(user)
            print("added the user")

        # like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        # if not created:
        #     if like.value=='Like':
        #         like.value='Unlike'
        #     else:
        #         like.value='Like'
        # else:
        #     like.value='Like'

        #     post_obj.save()
        #     like.save()

        data = {
            # 'value': like.value,
            'likes': post_obj.likes.all().count()
        }

        return JsonResponse(data, safe=False)
    # return redirect('posts:main-post-view')


def addPost(request):

    if request.method == 'POST':
        form = AddPosts(request.POST, initial={'user':request.user})
        if form.is_valid():
            form.save()
            return redirect('home-page')
    else:
        form = AddPosts(initial={'user':request.user})
        print(form)

    context = {
        'form':form,
    }
    return render(request, 'src_code/add_post.html', context)


def comments(request):
    return render(request, 'src_code.comments.html')



def register(request):
    if request.method == 'POST':
        print("Request POST ", request.POST)
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()
        
        new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])

        login(request, new_user)
        
        user = Detail.objects.create(user=request.user, name='Hello World ')
        return redirect('home-page')
    else:
        form = UserRegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'src_code/register.html', context)


def warning_page(request):
    return render(request, 'src_code/home.html')

def update_individualuser(request):
    initial_data = {
            'user':request.user,
        }
    if request.method == 'POST':
        form = DetailForm(request.POST, initial=initial_data)
        

        if form.is_valid():
            form.save()
        return redirect('home-page')
    else:
        form = DetailForm(initial=initial_data)

    context = {
        'form':form,
    }
    return render(request, 'src_code/update_user.html', context)



def check_message_intention(message):
    abusive_word_list = ["Cumbubble",
    "Fuck",
    "Shitbag",
    "Shit",
    "Piss off",
    "Asshole",
    "Dickweed",
    "Cunt",
    "bitch",
    "Bastard",
    "Bitch",
    "Damn",
    "Bollocks",
    "Bugger",
    "Cocknose",
    "Bloody hell",
    "Knobhead",
    "Choad",
    "Bitchtits",
    "Crikey",
    "Rubbish",
    "Pissflaps",
    "Shag",
    "Wanker",
    "Talking the piss",
    "Twat",
    "Arsebadger",
    "Jizzcock",
    "Cumdumpster",
    "Shitmagnet",
    "Scrote",
    "Twatwaffle",
    "Thundercunt",
    "Dickhead",
    "Shitpouch",
    "Jizzstain",
    "Nonce",
    "Pisskidney",
    "Wazzock",
    "Cumwipe",
    "Fanny",
    "Bellend",
    "Pisswizard",
    "Knobjockey",
    "Cuntpuddle",
    "Dickweasel",
    "Quim",
    "Bawbag",
    "Fuckwit",
    "Tosspot",
    "Cockwomble",
    "Twat face",
    "Cack",
    "Flange",
    "Clunge",
    "Dickfucker",
    "Fannyflaps",
    "Wankface",
    "Shithouse",
    "Gobshite",
    "Jizzbreath",
    "Todger",
    "Nutsack"]


    hate_word_lst = [
        'terrorist',
        'dead',
        'die',
        'kill',
        'murder',
        'rape',
        'horny',
        ''
    ]

    abuse_lst = []


    deny = ['no', 'not', 'none', 'eliminated', 'dont']


    lst_of_sentences = [
        'girls should not go to school',
        'women are not great as man',
        'women should work under man',
        '',
        '',
        '',
    ]

    for j in abusive_word_list:
        abuse_lst.append(j.lower())

    
    a_lst = message.split(" ")
    hate_flag = False
    abuse_flag = False
    for i in a_lst:
        if i.lower() in abuse_lst:
            hate_flag = True

    for i in a_lst:
        if i.lower() in hate_word_lst:
            hate_flag = True


    for i in a_lst:
        if i.lower() in deny:
            hate_flag = False

    for i in lst_of_sentences:
        if i == message:
            hate_flag = True
    if hate_flag:
        return "hate_speech"
    elif abuse_flag:
        return "abusive_speech"
    else:
        return "fine_speech"
