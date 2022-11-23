from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib import messages
from .forms import Signupform
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    if request.method == "POST":
        name = request.POST['username']
        passw = request.POST['password']
        user = authenticate(username = name,password = passw)
        if user:
            old_user = user.first_name.title()
            if user.policy.active == True:
                login(request, user)
                messages.success(request, 'Signin Successful!')
                return redirect('main')
            else:
                messages.success(request, f'Dear {old_user}, you have been barred from logging in, contact Admin for help.')
                return redirect('index')
        else:
            messages.warning(request,'Username/password incorrect')
            return redirect('index')
    return render(request, 'index.html')


def signout(request):
    logout(request)
    messages.success(request,'Logged Out')
    return redirect('index')


def main(request):
    incoming_debit = Checking.objects.filter(user__username = request.user.username).last()
    new_balance = incoming_debit.c_balance
    history = Checking.objects.filter(user__username = request.user.username, c_success =True).order_by('-id')
    bal = Saving.objects.filter(user__username = request.user.username).last()
    show_bal = bal.s_balance
    history2 = Saving.objects.filter(user__username = request.user.username, s_success =True).order_by('-id')
    added = Saving.objects.filter(user__username = request.user.username).last()
    new_add = int(added.s_balance)


    return render(request,'main.html', {
        'new_balance':new_balance,
        'history':history,
        'bal':bal,
        'show_bal':show_bal,
        'history2':history2,
        'new_add':new_add
        })


def signup(request):
    regform =Signupform()
    if request.method == 'POST':
        if regform.is_valid():
            regform.save()
            return redirect(request,'main')
        else:
            messages.error(request, regform.errors)
    return render(request,'signup.html',{'regform':regform})




def savings(request):
    bal = Saving.objects.filter(user__username = request.user.username).last()
    show_bal = int(bal.s_balance)
    
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        acc_no = request.POST['acc_no']
        acc_name = request.POST ['acc_name']
        purpose = request.POST ['purpose']
        bank = request.POST['bank']

        if show_bal >= amount:
            trans = Saving()
            trans.user= request.user
            trans.s_acc_holder = f'{request.user.first_name} {request.user.last_name}'
            trans.s_bank = bank
            trans.s_acc_name = acc_name
            trans.s_acc_num = acc_no
            trans.s_purpose = purpose
            trans.savings_account = True
            trans.s_balance = show_bal - amount
            trans.s_debit = amount
            trans.s_success = True
            trans.save()
            messages.success(request,'Successful')
            return redirect('main')
        else:
            messages.success(request,'Failed to Transfer')
            return redirect('main')
    return render(request,'savings.html',{'show_bal':show_bal})



def checkings(request):
    incoming_debit = Checking.objects.filter(user__username = request.user.username).last()
    new_balance = int(incoming_debit.c_balance)
    if request.method == 'POST':
        amt = int(request.POST['amount'])
        acc_no = request.POST['acc_no']
        acc_name = request.POST['acc_name']
        purpose = request.POST['purpose']
        bank = request.POST['bank']

        if new_balance >= amt: 
            transact = Checking()
            transact.user = request.user
            transact.c_acc_holder = f'{request.user.first_name} {request.user.last_name}'
            transact.c_bank = bank
            transact.c_acc_name = acc_name
            transact.c_acc_num =acc_no
            transact.c_purpose = purpose
            transact.checkings_account = True
            transact.c_debit  = amt
            transact.c_balance = new_balance - amt
            transact.c_success = True
            transact.save()
            messages.success(request,'Transaction successful!')
            return redirect('main')
        else:
                messages.success(request,'Insuffient Funds')
                return redirect('main')

    return render(request,'checkings.html',{'new_balance':new_balance})


def credit(request):
    incoming_credit = Checking.objects.filter(user__username = request.user.username).last()
    figure = int(incoming_credit.c_balance)
    if request.method == 'POST':
        amt = int(request.POST['amount'])
        purpose = request.POST['purpose']
        bank = request.POST['bank']

       
        increase = Checking()
        increase.user = request.user
        increase.c_acc_holder = f'{request.user.first_name} {request.user.last_name}'
        increase.c_purpose = purpose
        increase. c_bank = bank
        increase.c_credit = amt 
        increase.c_balance = figure + amt
        increase.c_success = True
        increase.checkings_account = True
        increase.save()
        messages.success(request,'Transaction successful!')
        return redirect('main')


    return render(request,'credit.html',{'figure':figure})


def savings_cd(request):
    added = Saving.objects.filter(user__username = request.user.username).last()
    new_add = int(added.s_balance)
    if request.method == "POST":
        amt = int(request.POST ['amount'])
        purpose = request.POST ['purpose']
        bank = request.POST ['bank']

        
        savingcd = Saving()
        savingcd.user = request.user
        savingcd.s_acc_holder = f'{request.user.first_name} {request.user.last_name}'
        savingcd.s_purpose = purpose
        savingcd.s_bank = bank
        savingcd.s_success = True
        savingcd.s_balance = new_add + amt
        savingcd.savings_account = True
        savingcd.s_credit = amt
        savingcd.save()
        messages.success(request, 'Credited Successfully')
        return redirect('main')
        
    return render(request,'savings_cd.html',{'new_add':new_add})


def cktrs(request):
    checkings = Checking.objects.filter(user__username = request.user.username).last()
    forc2 = int(checkings.c_balance)

    savings = Saving.objects.filter(user__username = request.user.username).last()
    tors = int(savings.s_balance)

    if request.method == "POST":
        amt = int(request.POST['amount'])
        purpose = request.POST['purpose']

        exttrns = Checking()
        exttrns.user = request.user
        exttrns.c_debit = amt
        exttrns.c_purpose = purpose
        exttrns.c_success = True
        exttrns.checkings_account = True
        exttrns.c_balance = forc2 - amt
        exttrns.save()
        

        intrn = Saving()
        intrn.user = request.user
        intrn.s_balance = amt + tors
        intrn.s_success = True
        intrn.savings_account = True
        intrn.save()

        messages.success(request,'Transfer Sucessful')
        return redirect('main')
        
    context = {
        'forc2':forc2,
        'tors':tors
    }
    return render(request, 'cktrs.html', context)



def me2me(request):
    mybal = Checking.objects.filter(user__username = request.user.username).last()
    newb = int(mybal.c_balance)
    

    if request.method == "POST":
        amt = int(request.POST ['amount'])
        name = request.POST  ['acc_name']
        purpose = request.POST  ['purpose']
        acc_no = request.POST ['acc_no']
        username = request.POST ['username']
        usid = User.objects.get(username = username)

        ext_trs = Checking()
        ext_trs.user = request.user
        ext_trs.c_debit = amt
        ext_trs.c_acc_holder = name
        ext_trs.c_purpose = purpose
        ext_trs.c_acc_num = acc_no
        ext_trs.c_success = True
        ext_trs.checkings_account = True
        ext_trs.c_balance = newb - amt
        ext_trs.save()


        newbd = Checking.objects.filter(user__username = usid).last()
        
        oldbalance = int(newbd.c_balance)
        receive = Checking()
        receive.user = usid
        receive.c_credit = amt
        receive.c_balance = oldbalance + amt
        receive.c_success = True
        receive.checkings_account = True
        receive.save()
        messages.success(request, 'Successful')
        return redirect('main')
        # else:
        #     messages.error(request, 'Incorrect Account Details')
        #     return redirect('me2me')

    context = {
        'newb':newb
    }
       
    return render(request,'me2me.html',context)
   

