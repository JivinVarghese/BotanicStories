from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


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


@login_required
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
