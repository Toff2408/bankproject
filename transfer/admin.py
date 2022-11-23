from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Checking)
class CheckingAdmin(admin.ModelAdmin):
    list_display = ['id','user','c_acc_holder','c_bank','c_acc_name','c_acc_num','c_purpose','checkings_account','c_credit','c_debit','c_balance','c_success','c_debit_date']

@admin.register(Saving)
class SavingsAdmin(admin.ModelAdmin):
    list_display = ['id','user','s_acc_holder','s_bank','s_acc_name','s_acc_num','s_purpose','savings_account','s_credit','s_debit','s_balance','s_success','s_debit_date']

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ['user','active']

