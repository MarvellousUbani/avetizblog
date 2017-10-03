# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode



class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=400)
    text = models.TextField(blank=True)
    post_pic = models.ImageField(upload_to='media', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    featured_post = models.BooleanField(default=False)
    trending_post = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default="Draft", choices=(('Draft','Draft'),('Published','Published'),('Submitted','Submitted')))
    category = models.ForeignKey('Category', null=True, blank=True)
    pageview=models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True, max_length=200)

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

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)
       


    def approve_comments(self):
        return self.comments.filter(approved_comment=True)


    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


    def get_cat_list(self):
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent

        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self',blank=True, null=True, related_name='children')

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])



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
        return self.post



class SubscribeEmail(models.Model):
    email=models.EmailField()
    active=models.BooleanField(default=False)
    token=models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    phone=models.CharField(max_length=200)
    message=models.TextField()






