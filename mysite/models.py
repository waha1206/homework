from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Maker(models.Model):
    name = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class PModel(models.Model):
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    url = models.URLField(default='https://i.imgur.com/CQtJpDU.png')
    def __str__(self):
        return self.name

class Product(models.Model):
    pmodel = models.ForeignKey(PModel, on_delete=models.CASCADE, verbose_name='型號')
    nickname = models.CharField(max_length=15, default='超值二手機', verbose_name='摘要')
    description = models.TextField(default='暫無說明')
    year = models.PositiveIntegerField(default=2016, verbose_name='出廠年份')
    price = models.PositiveIntegerField(default=0, verbose_name='價格')
    
    def __str__(self):
        return self.nickname
        
class PPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.CharField(max_length=20, default='產品照片')
    url = models.URLField(default='https://i.imgur.com/CQtJpDU.png')
    
    def __str__(self):
        return self.description
        
class Mood(models.Model):
    status = models.CharField(max_length=10, null=False)
    
    def __str__(self):
        return self.status

class Post(models.Model):
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, default='不願意透漏身分的人', verbose_name='暱稱')
    message = models.TextField(null=False, verbose_name='訊息')
    del_pass = models.CharField(max_length=10, help_text='要記住密碼')
    pub_time = models.DateTimeField(auto_now=True, verbose_name='發文時間')
    enabled = models.BooleanField(default=False, verbose_name = '審-核')
    
    def __str__(self):
        return self.message
        
#建立一個使用者 session

class User2(models.Model):
    name = models.CharField(max_length=20, null=False)
    email = models.EmailField()
    password = models.CharField(max_length=20, null=False)
    enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.PositiveIntegerField(default=160)
    male = models.BooleanField(default=False)
    website = models.URLField(null=True)
    
    def __str__(self):
        return self.user.username
#stmp.gmail.com
#django.core.mail.backends.smtp.EmailBackend
#django_mailgun.MailgunBackend
class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    note = models.TextField()
    ddate = models.DateField()
    
    def __str__(self):
        return "{}({})".format(self.ddate, self.user)