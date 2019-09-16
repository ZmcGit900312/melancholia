from django.db import models
from uuslug import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=128,unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True,max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)


class Page(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField(max_length=200)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    #这一行是必须的
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture= models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        return self.user.username