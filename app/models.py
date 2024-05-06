from django.db import models
import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal



class Category(models.Model):
    title = models.CharField(max_length=235, unique=True, null=False) 

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Categorie'  
    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(max_length=235, unique=True, null=False)  # Change primary_key=True to unique=True
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_per_1000 = models.DecimalField(default=Decimal('0'), max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    guide_prompt = models.CharField(max_length=255, null=True)


    class Meta:
        verbose_name_plural = "Services"
        verbose_name = 'Service'  

    def __str__(self):
        return self.title


class Customer(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=235, null=True,unique=True)
    first_name = models.CharField(max_length=235, null=True)
    last_name = models.CharField(max_length=235, null=True)
    email = models.EmailField(max_length=235, null=True)
    password = models.CharField(max_length=255, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')), blank=True)
    funds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_orders = models.IntegerField(default=0)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.username

    def authenticate_user(self, password):
        return check_password(password, self.password)

class Order(models.Model):
    status_choices = (
        ("Pending", "pending"),
        ("Progressing", "progressing"),
        ("Completed", "completed"),)
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    link = models.CharField(max_length=235, default='')
    status = models.CharField(max_length=235, choices=status_choices)
    date_created = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=None, null=True)
    charge = models.DecimalField(max_digits=50, decimal_places=10, default=0)
    class Meta:
        verbose_name = 'Order' 
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order for {self.customer.username} - {self.service.title} ({self.status})"
