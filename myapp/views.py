from django.shortcuts import render

# Create your views here.


def base(request):
    return render(request, 'base.html')

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            #ignore this line for now - this is for dummy data (will change it later)
            post.user = request.user if request.user.is_authenticated else User.objects.get(username='happy')  # Adjust as per your authentication logic
            post.save()

            # Create tags
            tags = request.POST.get('tags').split(',')
            for tag_name in tags:
                Tag.objects.create(post=post, tag_name=tag_name.strip())

            return redirect('view_post', post_id=post.post_id)
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})

def view_post(request, post_id):
    if request.method == 'POST':
        return redirect('create_post')  # Prevents re-posting on refresh

    try:
        post = Post.objects.get(post_id=post_id)
        tags = Tag.objects.filter(post=post)
    except Post.DoesNotExist:
        return redirect('create_post')  # Redirect to create_post if post not found

    return render(request, 'view_post.html', {'post': post, 'tags': tags})

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
