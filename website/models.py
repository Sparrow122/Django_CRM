from django.db import models
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User
# Create your models here

# class User_data(models.Model):
#     def get_user(self, user):
#         try:
#             return User.objects.filter(user)
#         except Http404:
#             return None

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=80)
    zipcode = models.CharField(max_length=20)
    added_by = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')
    
    def get_records(self, userid, pk=None):
        if (pk):
            try:
                return get_object_or_404(Record, id=pk, added_by=userid)
            except Http404:
                return None
        else:
            return Record.objects.filter(added_by=userid)
