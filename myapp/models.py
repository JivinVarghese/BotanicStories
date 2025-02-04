from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    interests = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='post_images/', blank=True)
    content = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)  # Add this line
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_title

    def bookmarked(self):
        return Bookmark.objects.filter(post=self, user=self.user).exists()

    def likes_count(self):
        return Like.objects.filter(post=self).count()

    def comments_count(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    def get_profile_img(self):
        try:
            url = UserDetail.objects.filter(user=self.user).first().profile_pic.url
        except:
            url = None
        return url


class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Bookmark(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.tag_name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name