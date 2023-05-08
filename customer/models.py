from django.db import models


# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=264, blank=False)
    last_name = models.CharField(max_length=264, blank=False)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50, blank=False)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.last_name

    # class Meta:
    #     db_table = u'customer'