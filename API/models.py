from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# the image will be stored in MEDIA_URL
def upload_path(instance, filname):
    return '/'.join(['covers', filname])


class Posts(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    cover = models.ImageField(upload_to=upload_path, blank=True, null=True)
    # many (post) to one (user) relationship
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts', default=1, blank=True, null=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    body = models.TextField(blank=False)
    author = models.ForeignKey(
        User, related_name='userComments', on_delete=models.CASCADE)
    post = models.ForeignKey(
        Posts, related_name='postComments', on_delete=models.CASCADE)

    def __str__(self):
        return self.body
