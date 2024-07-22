
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from .forms import *
from .models import *
from .decorators import *



# Create your views here.

def base(request):
    return render(request, 'base.html')



def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        detail_form = UserDetailForm(request.POST, request.FILES)

        if user_form.is_valid() and detail_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            user_detail = detail_form.save(commit=False)
            user_detail.user = user
            user_detail.save()

            return redirect('login')  # or wherever you want to redirect after registration
    else:
        user_form = UserForm()
        detail_form = UserDetailRegisterForm()

    return render(request, 'register.html', {'user_form': user_form, 'detail_form': detail_form})


@redirect_authenticated_user
def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a success page or home page
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_analytics(request):
    return render(request,'analytics.html')

  
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Create tags
            tags = request.POST.get('tags').split(',')
            for tag_name in tags:
                Tag.objects.create(post=post, tag_name=tag_name.strip())

            return redirect('view_post', post_id=post.post_id)
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})


# @login_required
def view_post(request, post_id):
    form = CommentForm(request.POST)
    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, post_id=post_id)
        comment.user = request.user  # Assigns the current logged-in user to the comment
        comment.save()
        return redirect('view_post', post_id=post_id)  # Prevents re-posting on refresh
        # return redirect('create_post')  # Prevents re-posting on refresh

    try:
        # post = Post.objects.get(post_id=post_id)
        post = get_object_or_404(Post, post_id=post_id)
        tags = Tag.objects.filter(post=post)
        user_detail = get_object_or_404(UserDetail, user=post.user)
    except Post.DoesNotExist:
        return redirect('')  # Redirect to create_post if post not found
    user_has_liked = Like.objects.filter(post=post, user=request.user).exists() if request.user.is_authenticated else False

    all_comments = Comment.objects.filter(post=post).order_by('-created_time')
    return render(request, 'view_post.html', {'post': post, 'tags': tags, 'form': form, 'comments': all_comments, 'user_detail': user_detail,'user_has_liked': user_has_liked})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    if request.user != post.user:
        return redirect('view_post', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            # Clear existing tags
            Tag.objects.filter(post=post).delete()
            # Add new tags
            tags = form.cleaned_data['tags']
            for tag_name in tags.split(','):
                tag, created = Tag.objects.get_or_create(post=post, tag_name=tag_name.strip())
            return redirect('view_post', post_id=post.post_id)
    else:
        form = PostForm(instance=post)
        # Join existing tags to show in the form
        existing_tags = ', '.join(post.tag_set.values_list('tag_name', flat=True))
        form.fields['tags'].initial = existing_tags
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})


# def comments(request):
#     return render(request, 'comment.html')


# def comments(request):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('comments')
#     else:
#         form = CommentForm()
#
#     return render(request, 'comment.html', {'form': form})


def generate_post_data(posts, user):
    user_bookmarks = Bookmark.objects.filter(user=user).values_list('post_id', flat=True) if user.is_authenticated else []
    post_data = []
    for post in posts:
        tags = Tag.objects.filter(post=post).values_list('tag_name', flat=True)

        user_detail = UserDetail.objects.filter(user=post.user).first()
        user_image = user_detail.profile_pic.url if user_detail and user_detail.profile_pic else None

        post_data.append({
            'id': post.post_id,
            'user_name': post.user.username,
            'user_image': user_image,
            'title': post.post_title,
            'subtitle': post.content[:400],
            'date' : post.create_date,
            'tags': list(tags),
            'image_url': post.image.url if post.image else None,
            'bookmarked': post.post_id in user_bookmarks,
            'likes_count': post.likes_count,
            'comments_count': post.comments_count
        })
    return post_data


def home(request):
    posts = Post.objects.all().order_by('-create_date')
    paginator = Paginator(posts, 3)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        post_data = generate_post_data(page_obj, request.user)
        html = render_to_string('post_list.html', {'posts': post_data})
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
            'num_posts': len(post_data)
        })

    page_obj = paginator.get_page(1)
    post_data = generate_post_data(page_obj, request.user)
    return render(request, 'home.html', {'posts': post_data, 'page_obj': page_obj})

@csrf_exempt
def bookmark_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        action = data.get('action')

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=403)

        post = get_object_or_404(Post, post_id=post_id)

        if action == 'add':
            Bookmark.objects.get_or_create(user=request.user, post=post)
            return JsonResponse({'status': 'added'})
        elif action == 'remove':
            Bookmark.objects.filter(user=request.user, post=post).delete()
            return JsonResponse({'status': 'removed'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id)
    # if request.user == comment.user or request.user.is_staff:
    if request.user == comment.user:
        if request.method == 'POST':
            comment.delete()
            messages.success(request, 'Comment deleted successfully.')
        return redirect('view_post', post_id=comment.post.post_id)
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('view_post', post_id=comment.post.post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id, post_id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully')
            return redirect('view_post', post_id=post_id)
        else:
            messages.error(request, 'There was an error updating your comment')


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_detail, created = UserDetail.objects.get_or_create(user=user)

    user_posts = Post.objects.filter(user=user).distinct()  # Fetch posts created by the user
    post_data = generate_post_data(user_posts, user)

    context = {
        'user': user,
        'user_detail': user_detail,
        'posts': post_data
    }
    return render(request, 'user_profile.html', context)


def about_user(request, username):
    user = get_object_or_404(User, username=username)
    user_detail, created = UserDetail.objects.get_or_create(user=user)
    context = {
        'user': user,
        'user_detail': user_detail
    }
    return render(request, 'about_user.html', context)


@login_required
def edit_profile(request):
    user_detail = UserDetail.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserDetailForm(request.POST, request.FILES, instance=user_detail)
        if form.is_valid():
            new_name = request.POST['name']
            if User.objects.filter(username=new_name).exclude(pk=request.user.pk).exists():
                form.add_error('name', 'This name is already taken. Please choose another.')
            else:
                form.save()
                request.user.username = new_name
                request.user.save()
                return redirect('user_profile', username=request.user.username)
    else:
        form = UserDetailForm(instance=user_detail)
    return render(request, 'edit_profile.html', {'form': form, 'user_detail': user_detail})

def search_posts(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        print('query ,', query)
        results = Post.objects.filter(Q(post_title__icontains=query) | Q(tag__tag_name__icontains=query)).distinct()
        data = [{'post_id': post.post_id, 'post_title': post.post_title} for post in results]
        print("data", data)
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def like_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        action = data.get('action')

        post = get_object_or_404(Post, post_id=post_id)

        if action == 'add':
            Like.objects.get_or_create(user=request.user, post=post)
            return JsonResponse({'status': 'added', 'likes_count': post.likes_count()})
        elif action == 'remove':
            Like.objects.filter(user=request.user, post=post).delete()
            return JsonResponse({'status': 'removed', 'likes_count': post.likes_count()})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def about(request):
    return render(request, 'about.html')

def landing_page(request):
    return render(request, 'landing_page.html')


@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = ContactForm(data)

        if form.is_valid():
            contact = form.save()  # This should save the contact to the database
            return JsonResponse({'status': 'success', 'message': 'Your message has been submitted successfully!'}, status=201)
        else:
            return JsonResponse({'error': form.errors}, status=400)

    # Handle GET request and render the contact page
    form = ContactForm()  # Create an empty form instance
    return render(request, 'contact.html', {'form': form})

  