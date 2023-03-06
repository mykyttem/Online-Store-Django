from django.shortcuts import render, redirect
from django.template import loader
from .models import Registration
from django.http import HttpResponse
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login


# Create your views here.
def accounts_users(request):
    if request.method == 'POST':
        login_user = request.POST['login']
        email_user = request.POST['email']
        password_user = request.POST['password']

        # hashed password
        hashed_password = make_password(password_user)


        if len(login_user) < 3:
            return HttpResponse('Error, login name is too short')
        else:
            new_account = Registration(login_user=login_user, email_user=email_user, password_user=hashed_password)
            new_account.save()
            return redirect('sign_in')

            
        

    return render(request, 'registration.html', {})



def sign_in(request):
    if request.method == 'POST':
        login_user = request.POST['login']
        email_user = request.POST['email']
        password_user = request.POST['password']

        # search login user, from DB
        search_login = Registration.objects.filter(
        Q(login_user = f'{login_user}'))


        if not search_login:
            messages.success(request, "Not found account/not correct password")
            return redirect('sign_in')
        
        else:
            # get user from DB
            user = Registration.objects.get(login_user=login_user)
            # check password
            if check_password(password_user, user.password_user):
                return redirect('my_profile')
            else:
                messages.success(request, "Incorrect password")
                return redirect('sign_in')



    return render(request, 'sign_in.html', {})



def my_profile(request):
    return render(request, 'my_profile.html')

