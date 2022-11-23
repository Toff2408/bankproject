from django.urls import path
from . views import *

urlpatterns = [
    path('',index,name = 'index'),
    path('main',main,name = 'main'),
    path('signup',signup,name = 'signup'),
    path('checkings',checkings,name = 'checkings'),
    path('savings',savings,name = 'savings'),
    path('credit',credit,name = 'credit'),
    path('signout',signout,name='signout'),
    path('savings_cd',savings_cd,name='savings_cd'),
    path('cktrs',cktrs,name='cktrs'),
    path('me2me',me2me,name='me2me'),
]