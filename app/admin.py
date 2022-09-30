from django.contrib import admin
# Register your models here.
from .models import Account,Box
admin.site.register(Account)
admin.site.register(Box)