from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Öğrenciye ait ekstra bilgiler
class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)

    def __str__(self):
        return self.user.first_name + ' [' + self.enrollment + ']'

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id

# Kitap modeli
class Book(models.Model):
    catchoice = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
    ]
    name = models.CharField(max_length=50)
    isbn = models.BigIntegerField()
    author = models.CharField(max_length=50)
    category = models.CharField(max_length=30, choices=catchoice, default='education')

    def __str__(self):
        return f"{self.name} [{self.isbn}]"

# Kitap verildiğinde kaç gün sonra iade edilecek?
def get_expiry():
    return datetime.today() + timedelta(days=30)

# Ödünç alınan kitaplar
class IssuedBook(models.Model):
    enrollment = models.CharField(max_length=30)
    isbn = models.CharField(max_length=30)
    issuedate = models.DateField(auto_now=True)
    expirydate = models.DateField(default=get_expiry)
    
    statuschoice = [
        ('Issued', 'Issued'),
        ('Returned', 'Returned'),
    ]
    status = models.CharField(max_length=20, choices=statuschoice, default='Issued')

    def __str__(self):
        return self.enrollment
