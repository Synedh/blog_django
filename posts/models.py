from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=1024)

    def __str__(self):
        return self.tag


class Post(models.Model):
    title = models.CharField(max_length=1024)
    content = models.TextField()
    image = models.CharField(max_length=1024)
    author = models.CharField(max_length=1024)
    view = models.IntegerField(default=0)
    show_post = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
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
    validated = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')

    def all_validated(self):
        return self.filter(validated=True)

    def __str__(self):
        return self.content[0:20] + "..."

    class Meta:
        ordering: ('pub_date',)


class Option(models.Model):
    nb_post_page = models.IntegerField(default=5)
    message = models.TextField(default="")
    recent_posts = models.BooleanField(default=True)
    most_used_tags = models.BooleanField(default=True)
    used = models.BooleanField(default=False)
