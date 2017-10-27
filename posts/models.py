from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=1024)

    def __str__(self):
        return self.tag


class Post(models.Model):
    title = models.CharField(max_length=1024)
    content = models.TextField()
    author = models.CharField(max_length=1024)
    view = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    tag = models.ManyToManyField(Tag)

    def content_in_index(self):
        return self.content.split('<p>')[1]

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('pub_date',)


class Commentary(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=1024)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.content[0:20] + "..."

    class Meta:
        ordering: ('pub_date',)
