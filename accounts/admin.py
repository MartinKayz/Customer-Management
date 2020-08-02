from django.contrib import admin
from .models import Customer,Product,Orders

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Orders)

