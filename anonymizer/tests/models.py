import uuid

from django.db import models


class Other(models.Model):
    pass


class EverythingModel(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    username = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    o1 = models.ForeignKey(Other)
    lorem = models.TextField()
    similar_lorem = models.TextField()
    unique_lorem = models.TextField(unique=True)
    some_varchar = models.CharField(max_length=5)
    no_varchar = models.CharField()
    birthday = models.DateTimeField()
    age = models.PositiveSmallIntegerField()
    icon = models.ImageField(upload_to='.')
    some_datetime = models.DateTimeField()
    some_date = models.DateField()
    sex = models.CharField(max_length=1, choices=[('M', 'Male'),
                                                  ('F', 'Female')])
    price = models.DecimalField(decimal_places=2, max_digits=10)
    binary = models.BinaryField()
    uuid = models.UUIDField(default=uuid.uuid4)
    boolean = models.BooleanField()
    small_integer = models.SmallIntegerField()
    positive_small_integer = models.PositiveSmallIntegerField()
    postcode = models.CharField(max_length=9)
    country = models.CharField(max_length=45)
    first_name = models.CharField(max_length=5)
    last_name = models.CharField(max_length=5)
    similar_email = models.EmailField()
    similar_email_other = models.EmailField()
    phonenumber = models.CharField(max_length=10)
    last_name = models.CharField(max_length=11)
    street_address = models.CharField(max_length=15)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=9)
    company = models.CharField(max_length=30)
    similar_datetime = models.DateTimeField()
    similar_date = models.DateField()
