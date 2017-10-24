from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=1024)
    content = models.TextField()
    author = models.CharField(max_length=1024)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title + " - " + self.content[0:20] + "..."
        

class Commentary(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=1024)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.content[0:20] + "..."
