from django.db import models


class CustomField(models.TextField):
    PREFIX = 'custom field!'

    def from_db_value(self, value, expression, connection, context):
        if not value.startswith(self.PREFIX):
            raise ValueError('Incorrect prefix!! %s' % value)

        return value[len(self.PREFIX):]

    def get_prep_value(self, value):
        return self.PREFIX + value


class Other(models.Model):
    pass


class EverythingModel(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    username = models.CharField(max_length=20, unique=True)
    address_city = models.CharField(max_length=50)
    address_post_code = models.CharField(max_length=10)
    address = models.TextField()
    o1 = models.ForeignKey(Other)
    something = models.TextField()
    something_else = models.TextField()
    some_varchar = models.CharField(max_length=5)
    birthday = models.DateTimeField()
    age = models.PositiveSmallIntegerField()
    icon = models.ImageField(upload_to='.')
    some_datetime = models.DateTimeField()
    some_date = models.DateField()
    sex = models.CharField(max_length=1, choices=[('M', 'Male'),
                                                  ('F', 'Female')])
    price = models.DecimalField(decimal_places=2, max_digits=10)
    custom = CustomField()
