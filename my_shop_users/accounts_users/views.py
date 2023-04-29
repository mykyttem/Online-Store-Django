from django.shortcuts import render, redirect

from .models import Registration
from items.models import Items

from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from datetime import datetime 


#TODO: добавити більше даних для користувача
def accounts_users(request):
    if request.method == 'POST':
        login_user = request.POST['login']
        email_user = request.POST['email']
        password_user = request.POST['password']

        # hashed password
        hashed_password = make_password(password_user)

        # search email-dublicate user, from DB
        search_email_dublicate = Registration.objects.filter(
        email_user = email_user)

        # search login-dublicate user, from DB
        search_login_dublicate = Registration.objects.filter(
        login_user = login_user)


        if len(login_user) < 3:
            return HttpResponse('Error, login name is too short')
        if search_email_dublicate or search_login_dublicate:
            messages.success(request, "Така пошта все зарегестрована")
        else:
            new_account = Registration(login_user=login_user, email_user=email_user, password_user=hashed_password)
            new_account.save()
            return redirect('sign_in')


    return render(request, 'registration.html', {})


def sign_in(request):
    if request.method == 'POST':
        login_user = request.POST['login']
        password_user = request.POST['password']

        search_login = Registration.objects.filter(login_user = login_user)

        if not search_login:
            messages.success(request, "Not found login/not correct password")
            return redirect('sign_in')
        else:
            user = Registration.objects.get(login_user=login_user)
            # check password, and save session
            if check_password(password_user, user.password_user):
                request.session['login'] = user.login_user
                request.session['email'] = user.email_user 
                request.session['id'] = user.id

                return redirect('my_profile')
            else:
                return redirect('sign_in')


    return render(request, 'sign_in.html', {})


def my_profile(request):
    id_user = request.session.get('id')
    if not id_user:
        return HttpResponse('Ви забули увійти в аккаунт')
    else:
        login_user = request.session.get('login')
        email_user = request.session.get('email')

        # button
        logout_profile = request.POST.get('logout_profile')
        delete_item = request.POST.get('delete_item') 

        # get field from items edit
        item_id = request.POST.get('item_id')
        name_items_get_edit = request.POST.get('name_items')
    
        myitems = Items.objects.filter(author_id_item=id_user).values 
    
        context = {
            'login_user': login_user,
            'email_user': email_user,    
            'id_user': id_user,
            'myitems': myitems
            }
        
        
        if request.method == 'POST':
            if logout_profile: 
                request.session.flush() # logout button - delete session
                return redirect('my_profile')


            if delete_item:
                item_id_get = Items.objects.filter(id=item_id).first() # get only ті items, які create user
                if item_id_get and item_id_get.author_id_item == id_user: # delete item той який належить user
                    item_id_get.delete()
                    
                return redirect('my_profile')


            if edit_item:            
                return redirect(f'edit_item/{item_id}/{name_items_get_edit}/')
            

    return render(request, 'my_profile.html', context)


def edit_profile(request):
    id_user = request.session.get('id')
    if not id_user:
        return HttpResponse('Увійдіть в кабінет')
    else:
        user_account = Registration.objects.filter(id=id_user).values()

        if request.method == 'POST':
            edit_login = request.POST['edit_login']
            edit_email = request.POST['edit_email']

            actual_password = request.POST['actual_password']
            edit_password_confirm = request.POST['password_confirm']
            
            edit_account = Registration.objects.get(id=id_user)
            for i in user_account:
                if edit_account:
                    hashed_password = make_password(edit_password_confirm)

                    edit_account.login_user = edit_login
                    edit_account.email_user = edit_email
                    edit_account.password_user = hashed_password
                    
                    if check_password(actual_password, i['password_user']):
                        edit_account.save()
                        messages.success(request, 'Увійдіть знову, для оновлення даних у профілі')
                        return redirect('sign_in')
                    elif len(edit_login) < 3:
                        messages.success(request, "Короткий логін")
                    else:
                        messages.success(request, "Поточний пароль не вірний")


        context = {
            'user_account': user_account 
        }


    return render(request, 'edit_profile.html', context)


def see_profile_seller(request, id, login):
    items_seller = Items.objects.filter(author_id_item=id).values()        

    context = {
        'id': id,
        'login': login,
        'items_seller': items_seller
    }

    return render(request, 'profile_seller.html', context)


def create_item(request):
    id_seller = request.session.get('id')
    seller = Registration.objects.filter(id=id_seller).values()
    
    if not id_seller:
        return HttpResponse('Увійдіть в кабінет')
    else:
        if request.method == 'POST':
            name_item = request.POST['name_item']
            description_item = request.POST['description_item']
            category_items = request.POST['category_items']

            phone_user = request.POST['phone_user']
            price_item = request.POST['price_item']
            guarantee = request.POST['guarantee_period']

            amount_item = request.POST['amount_item']

            status_availability = request.POST.get('status_availability') 
            state_new = request.POST.get('state_new')
      
            date = datetime.now()

            new_item = Items(name_items=name_item, description_items=description_item, category_items=category_items, phone=phone_user, price=price_item, joined_date=date, author_id_item=id_seller,
                             status='В наявності' if status_availability == 'on' else 'Готов к відправки', state='Новий' if state_new == 'on' else 'Вживаний', guarantee=guarantee, amount_item=amount_item)
            new_item.save()


            return redirect('my_profile')


    return render(request, 'create_item.html', {'seller': seller})


def edit_item(request, item_id, name_items_get_edit):
    id_seller = request.session.get('id')
    if not id_seller:
        return HttpResponse('Увійдіть в акаунт')
    else:
        find_item = Items.objects.filter(id=item_id)
        find_seller = Registration.objects.filter(id=id_seller)

        context = {'find_item': find_item.values(), 'find_seller': find_seller}

        if request.method == 'POST':
            name_item_edit = request.POST['name_item']
            description_item_edit = request.POST['description_item']
            category_items_edit = request.POST['category_items']
            phone_user_edit = request.POST['phone_user']
            price_item_edit = request.POST['price_item']
            guarantee_period = request.POST['guarantee_period']
            amount_item = request.POST['amount_item']


            find_item = find_item.first()
            if find_item:
                find_item.name_items = name_item_edit
                find_item.description_items = description_item_edit
                find_item.category_items = category_items_edit
                find_item.phone = phone_user_edit
                find_item.price = price_item_edit
                find_item.guarantee = guarantee_period
                find_item.amount_item = amount_item


                find_item.save()

                return redirect('my_profile')
            
            return redirect('my_profile')


    return render(request, 'edit_item.html', context)