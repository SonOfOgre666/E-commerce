from django.contrib import admin
from .models import (Customer, Order, Service, Category)


admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Order)
