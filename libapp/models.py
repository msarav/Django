from django.db import models

# Create your models here.

import datetime

from django.contrib.auth.models import User

class Libuser(User):
    PROVINCE_CHOICES = (
        ('AB','Alberta'),  # The first value is actually stored in db, the second is descriptive
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    # age = models.IntegerField()
    phone = models.IntegerField(null=True)

    #----------- Addtional Fields ------------------- #

    postalcode = models.CharField(max_length=7,null=True, blank=True)

    # ----------------------------------------------- #

    def __str__(self):
        return self.get_full_name()


class Libitem(models.Model):
    TYPE_CHOICES = (
        ('Book', 'Book'),
        ('DVD','DVD'),
        ('Other', 'Other'),
    )
    title = models.CharField(max_length=100)
    itemtype = models.CharField(max_length=6, choices=TYPE_CHOICES, default='Book')
    checked_out=models.BooleanField(default=False)

    user=models.ForeignKey(Libuser, default=None, null=True, blank=True)
    #user = models.ManyToManyField(Libuser)

    duedate = models.DateField(default=None, null=True, blank=True)
    last_chkout = models.DateField(default=None, null=True, blank=True)
    date_acquired = models.DateField(default=datetime.date.today())
    pubyr = models.IntegerField()
    #overdue = models.BooleanField(default=False)

    # ----------- Addtional Fields ------------------- #

    num_chkout= models.IntegerField(default=0)

    # ----------------------------------------------- #

    def __str__(self):
        return self.title + ' bya ' + self.itemtype

    def overdue(self):
        if self.checked_out:
            if str(self.duedate) != 'None' and self.duedate < datetime.date.today():
                return 'Yes'
            elif str(self.duedate) == 'None':
                self.duedate = datetime.date.today()
                return 'No'
            else:
                return 'No'
        else:
            return 'Not Checked out'

class Book(Libitem):
    CATEGORY_CHOICES = (
        (1, 'Fiction'),
        (2, 'Biography'),
        (3, 'Self Help'),
        (4, 'Education'),
        (5, 'Children'),
        (6, 'Teen'),
        (7, 'Other'),
    )
    author = models.CharField(max_length=100)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)

    def __str__(self):
        return self.title + ' bya ' + self.author


class Dvd(Libitem):

    RATING_CHOICES = (
        (1, 'G'),
        (2, 'PG'),
        (3, 'PG-13'),
        (4, '14A'),
        (5, 'R'),
        (6, 'NR'),
    )
    maker = models.CharField(max_length=100)
    duration = models.IntegerField(default=1)
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)

    def __str__(self):
        return self.title + ' bya ' + self.maker


class Suggestion(models.Model):

    TYPE_CHOICES = (
        (1, 'Book'),
        (2,'DVD'),
        (3, 'Other'),
    )
    title = models.CharField(max_length=100)
    pubyr = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(default=1, choices=TYPE_CHOICES)
    cost = models.IntegerField()
    num_interested = models.IntegerField()
    comments = models.TextField()

    def __str__(self):
        return self.title #+ ' of type ' + self.type