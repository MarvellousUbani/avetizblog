from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver



class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    post_pic = models.ImageField(upload_to='media', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    featured_post = models.BooleanField(default=False)
    trending_post = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default="Draft", choices=(('Draft','Draft'),('Published','Published'),('Submitted','Submitted')))
    category = models.CharField(max_length=100, default="News", choices=(('News', 'News'),('Trend','Trend'),('Weird Houses', 'Weird Houses'),('My Story', 'My Story'),('Business','Business'),('Entertainment','Entertainment'),('Around the Web','Around the Web'),('Advertise with Us','Advertise with Us')))

    def publish(self):
        if self.post_pic and self.text:
            self.published_date = timezone.now()
            self.status = 'Published'
            self.save
            return True
        else:
            return False

    def submit(self):
        if self.post_pic and self.text:
            self.status='Submitted'
            self.save()
            return True
        else:
            return False
       


    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})


    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text





