from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.IntegerField(default=None, null=True)
    available = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, default=None)
    return_date = models.DateField(default=None, null=True)

    def __str__(self) -> str:
        return self.name

    def update_availablity(self, is_available):
        self.available = is_available
        self.save()
    
    def update_return_date(self, days):
        if days:
            self.return_date = date.today() + timedelta(days=days)
        else:
            self.return_date = None
        self.save()
    
    def update_user(self, user):
        self.user = user
        self.save()
    
    def issue_book(self, days, user):
        self.update_availablity(False)
        self.update_return_date(days) 
        self.update_user(user)
    
    def return_book(self):
        self.update_availablity(True)
        self.update_return_date(None)
        self.update_user(None)