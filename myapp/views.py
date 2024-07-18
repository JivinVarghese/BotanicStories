from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

def base(request):
    return render(request, 'base.html')


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            #ignore this line for now - this is for dummy data (will change it later)
            post.user = request.user if request.user.is_authenticated else User.objects.get(
                username='happy')  # Adjust as per your authentication logic
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
        post = Post.objects.get(post_id=post_id)
        tags = Tag.objects.filter(post=post)
    except Post.DoesNotExist:
        return redirect('create_post')  # Redirect to create_post if post not found

    all_comments = Comment.objects.filter(post=post).order_by('-created_time')
    return render(request, 'view_post.html', {'post': post, 'tags': tags, 'form': form, 'comments': all_comments})


def edit_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('view_post', post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post_id': post_id})


def delete_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('base')
    return render(request, 'delete_post.html', {'post': post})


# def comments(request):
#     return render(request, 'comment.html')


def comments(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comments')
    else:
        form = CommentForm()

    return render(request, 'comment.html', {'form': form})


# def home(request):
#     # Fetch posts from the database, ordered by creation date (newest first)
#     posts = Post.objects.order_by('-created_at')[:10]  # Limit to 10 most recent posts
#
#     # Prepare the data for the template
#     post_data = []
#     for post in posts:
#         post_info = {
#             'id': post.post_id,
#             'user_name': post.user.username,
#             'user_image': post.user.profile.image.url if hasattr(post.user, 'profile') and post.user.profile.image else None,
#             'title': post.title,
#             'subtitle': post.subtitle,
#             'likes': post.likes.count(),
#             'comments': post.comments.count(),
#             'date': post.created_at.strftime('%b %d'),  # Format date as 'May 30'
#             'tags': list(post.tags.values_list('tag_name', flat=True)),
#             'image_url': post.image.url if post.image else None
#         }
#         post_data.append(post_info)
#
#     return render(request, 'home.html', {'posts': post_data})


# ...................................
# temporary view for home is below
# ...................................

def home(request):
    # Dummy content
    posts = [
        {
            'id': 1,
            'user_name': 'Malhar Raval',
            'user_image': None,  # Add image URL here if available
            'title': 'A Founder Who Just Raised a $3 Million Seed Round Showed Me the New Way Startups Are Pitching VCs',
            'subtitle': 'The ideal structure for fundraising pitches is constantly changing, and the newest iteration has clearly arrived.',
            'likes': 1100,
            'comments': 34,
            'date': 'May 30',
            'tags': ['Entrepreneurship', 'Startup', 'VC'],
            'image_url': '/static/images/1.jpg'  # Make sure to place your image in the static/images directory
        },
        {
            'id': 2,
            'user_name': 'Harsh Sachala',
            'user_image': None,
            'title': 'A Founder Who Just Raised a $3 Million Seed Round Showed Me the New Way Startups Are Pitching VCs',
            'subtitle': 'The ideal structure for fundraising pitches is constantly changing, and the newest iteration has clearly arrived.',
            'likes': 44,
            'comments': 3,
            'date': 'April 23',
            'tags': ['Fundraising', 'Innovation'],
            'image_url': '/static/images/2.jpg'
        },
        {
            'id': 3,
            'user_name': 'Akshar Patel',
            'user_image': None,
            'title': 'A Founder Who Just Raised a $3 Million Seed Round Showed Me the New Way Startups Are Pitching VCs',
            'subtitle': 'The ideal structure for fundraising pitches is constantly changing, and the newest iteration has clearly arrived.',
            'likes': 222121,
            'comments': 3444,
            'date': 'May 10',
            'tags': ['Pitching', 'Business'],
            'image_url': '/static/images/3.jpg'
        },
        # Add more posts here
    ]
    return render(request, 'home.html', {'posts': posts})


@login_required
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
    context = {
        'user': user,
        'user_detail': user_detail
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
            form.save()
            request.user.username = request.POST['name']
            request.user.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserDetailForm(instance=user_detail)
    return render(request, 'edit_profile.html', {'form': form, 'user_detail': user_detail})


def search_posts(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        print('query ,',query)
        results = Post.objects.filter(Q(post_title__icontains=query) | Q(tag__tag_name__icontains=query)).distinct()
        data = [{'post_id': post.post_id, 'post_title': post.post_title} for post in results]
        print("data",data)
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def landing_page(request):
    return render(request, 'landing_page.html')