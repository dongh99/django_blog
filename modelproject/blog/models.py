from django.db import models
from account.models import CustomUser
from django.utils import timezone

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length= 200)
    writer = models.CharField(max_length = 10)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to="blog/", blank=True, null=True)

    def __str__(self): 
        return self.title

    def summary(self):
        return self.body[:100]

class Comment(models.Model):
    post=models.ForeignKey(Blog, null=True,blank=True, on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    content=models.TextField()
    created_time=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.content