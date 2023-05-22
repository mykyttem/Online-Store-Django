from functools import wraps

from django.shortcuts import render, redirect

from .models import Registration
from items.models import Items
from client_service.models import Chat_UserSeller, MessageChat

from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password


# decorator, checking session on user, whether the user is logged into the account
def auth_user(f):
    @wraps(f)
    def decorated_if_session(request, *args, **kwargs):
        # checking sesion
        id_user = request.session.get('id')
        if 'id' not in request.session:
            return redirect('/sign_in')
        return f(request, id_user, *args, **kwargs)
    
    return decorated_if_session


def registration(request):
    if request.method == 'POST':
        login_user = request.POST['login']
        email_user = request.POST['email']
        password_user = request.POST['password']
        avatar_user = request.FILES.get('avatar') 

        # hashed password
        hashed_password = make_password(password_user)

        # search email-dublicate user, from DB
        search_email_dublicate = Registration.objects.filter(
        email_user = email_user)

        # search login-dublicate user, from DB
        search_login_dublicate = Registration.objects.filter(
        login_user = login_user)


        if len(login_user) < 3:
            return messages.success('Error, login name is too short')
        if search_email_dublicate or search_login_dublicate:
            messages.success(request, "Така пошта все зарегестрована")
        else:
            if avatar_user:
                new_account = Registration(login_user=login_user, email_user=email_user, password_user=hashed_password, avatar_user=avatar_user)
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


@auth_user
def my_profile(request, id_user):
    account = Registration.objects.filter(id=id_user).values()

    # button
    logout_profile = request.POST.get('logout_profile')
    delete_item = request.POST.get('delete_item') 

    # get field from items edit
    item_id = request.POST.get('item_id')
    name_items_get_edit = request.POST.get('name_items_get_edit')

    myitems = Items.objects.filter(author_id_item=id_user).values() 

    context = {
        'account': account,
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


@auth_user
def edit_profile(request, id_user):
    user_account = Registration.objects.filter(id=id_user).values()

    if request.method == 'POST':
        edit_login = request.POST['edit_login']
        edit_email = request.POST['edit_email']

        actual_password = request.POST['actual_password']
        edit_password_confirm = request.POST['password_confirm']
        edit_avatar = request.FILES.get('edit_avatar') 

        edit_account = Registration.objects.get(id=id_user)
        for i in user_account:
            if edit_account:

                edit_account.login_user = edit_login
                edit_account.email_user = edit_email

                # checking edit to empty field or None
                edit_account.password_user = make_password(actual_password) if edit_password_confirm == '' else make_password(edit_password_confirm)
                if not edit_avatar == None:
                    edit_account.avatar_user = edit_avatar

                
                if check_password(actual_password, i['password_user']):
                    edit_account.save()
                    request.session.flush()
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


def my_chats(request, id):
    if not id:
        return redirect('/sign_in')

    # get data from url 
    chats = Chat_UserSeller.objects.filter(Q(id_buyer=id) | Q(id_seller=id)).values()  
    messages_chats = MessageChat.objects.values()
    search_interlocutor = Registration.objects.all()  

    context = {
        'chats': chats, 
        'message': messages_chats,
        'interlocutor': search_interlocutor, 
        'my_id': id
    }

    return render(request, 'my_chats.html', context)


def see_profile_seller(request, id, login):
    items_seller = Items.objects.filter(author_id_item=id).values()        

    context = {
        'id': id,
        'login': login,
        'items_seller': items_seller,
    }

    return render(request, 'profile_seller.html', context)

@auth_user
def create_item(request, id_user):
    seller = Registration.objects.filter(id=id_user).values()

    if request.method == 'POST':
        name_item = request.POST['name_item']
        description_item = request.POST['description_item']
        category_items = request.POST['category_items']

        phone_user = request.POST['phone_user']
        price_item = request.POST['price_item']
        
        amount_item = request.POST['amount_item']
        photo = request.FILES.get('photo')

        # promotion code
        promotion_code = request.POST['promotion_code']
        amount_users_type = request.POST['amount_users_type']
        guarantee = request.POST['guarantee_period']
        at_what_price = request.POST['at_what_price']
        validity_period_promocode = request.POST['validity_period_promocode']

        status_availability = request.POST.get('status_availability') 
        state_new = request.POST.get('state_new')
    

        new_item = Items(name_items=name_item, description_items=description_item, category_items=category_items, phone=phone_user, price=price_item, author_id_item=id_user,
                            status='В наявності' if status_availability == 'on' else 'Готов к відправки', 
                            state='Новий' if state_new == 'on' else 'Вживаний', 
                            guarantee=None if guarantee == '' else guarantee, 
                            amount_item=amount_item,
                            promotion_code=None if promotion_code == '' else promotion_code, 
                            amount_type_promotion_code=None if amount_users_type == '' else amount_users_type, 
                            at_what_price=None if at_what_price == '' else at_what_price, 
                            validity_period_promocode=None if validity_period_promocode == '' else validity_period_promocode, 
                            photo='/items/no_photo_item.png' if photo == '' else photo)
        new_item.save()


        return redirect('my_profile')


    return render(request, 'create_item.html', {'seller': seller})

@auth_user
def edit_item(request, id_user, name_items_get_edit, item_id):
    find_item = Items.objects.filter(id=item_id)
    find_seller = Registration.objects.filter(id=id_user)

    context = {'find_item': find_item.values(), 
                'find_seller': find_seller, 
                'name_items_get_edit': name_items_get_edit
            }
    
    old_price = [i['price'] for i in find_item.values()]          

    if request.method == 'POST':
        name_item_edit = request.POST['name_item']
        description_item_edit = request.POST['description_item']
        category_items_edit = request.POST['category_items']
        phone_user_edit = request.POST['phone_user']
        price_item_edit = request.POST['price_item']
        guarantee_period = request.POST['guarantee_period']
        amount_item = request.POST['amount_item']

        # promotion code
        promotion_code_edit = request.POST['promotion_code_edit']
        amount_users_type_edit = request.POST['amount_users_type_edit']
        at_what_price_edit = request.POST['at_what_price_edit']
        validity_period_promocode_edit = request.POST['validity_period_promocode_edit']


        find_item = find_item.first()
        if find_item:
            # save new data
            find_item.name_items = name_item_edit
            find_item.description_items = description_item_edit
            find_item.category_items = category_items_edit

            find_item.phone = phone_user_edit
            find_item.price = price_item_edit

            find_item.guarantee = None if guarantee_period == '' else guarantee_period
            find_item.amount_item = amount_item

            find_item.promotion_code = promotion_code_edit
            find_item.amount_type_promotion_code = None if amount_users_type_edit == 'None' else amount_users_type_edit
            find_item.at_what_price = None if at_what_price_edit == 'None' else at_what_price_edit
            find_item.validity_period_promocode = None if validity_period_promocode_edit == 'None' else validity_period_promocode_edit
            

            for old in old_price:
                find_item.old_price = old
                find_item.discount = ((old - int(price_item_edit)) / old) * 100 
                    
            find_item.save()


            return redirect('my_profile')

        return redirect('my_profile')
    

    return render(request, 'edit_item.html', context)