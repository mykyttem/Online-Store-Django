from django.shortcuts import render, redirect

from .models import Registration
from items.models import Items
from client_service.models import Order_Items

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
    login_user = request.session.get('login')
    email_user = request.session.get('email')
    id_user = request.session.get('id')


    # button
    logout_profile = request.POST.get('logout_profile')
    delete_item = request.POST.get('delete_item') 

    # global variabes for edit item
    global item_id

    global name_items_get_edit
    global description_get_edit
    global category_get_items_edit

    global phone_get_edit
    global price_get_edit

    # get field from items edit
    item_id = request.POST.get('item_id')
    name_items_get_edit = request.POST.get('name_items')
    description_get_edit = request.POST.get('description_items')
    category_get_items_edit = request.POST.get('category_items')
    phone_get_edit = request.POST.get('phone')
    price_get_edit = request.POST.get('price')    


    if login_user == None:
        return HttpResponse('Ви забули увійти в аккаунт')
    
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
            return redirect('edit_item')
        

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
    id_user = request.session.get('id')
    
    if not id_user:
        return HttpResponse('Увійдіть в кабінет')
    else:
        if request.method == 'POST':
            name_item = request.POST['name_item']
            description_item = request.POST['description_item']
            category_items = request.POST['category_items']


            phone_user = request.POST['phone_user']
            price_item = request.POST['price_item']

            id_user = request.session.get('id')        

            # date create item
            date = datetime.now()

            new_item = Items(name_items=name_item, description_items=description_item, category_items=category_items, phone=phone_user, price=price_item, joined_date=date, author_id_item=id_user)
            new_item.save()


            return redirect('my_profile')


    return render(request, 'create_item.html', {})


def edit_item(request):
    id_user = request.session.get('id')
    if not id_user:
        return HttpResponse('Увійдіть в акаунт')
    else:
        context = {
            'name_items_get_edit': name_items_get_edit,
            'description_get_edit': description_get_edit,
            'category_get_items_edit': category_get_items_edit,        
            'phone_get_edit': phone_get_edit,
            'price_get_edit': price_get_edit
        }
        

        if request.method == 'POST':
            name_item_edit = request.POST['name_item_edit']
            description_item_edit = request.POST['description_item_edit']
            category_items_edit = request.POST['category_items_edit']
            phone_user_edit = request.POST['phone_user_edit']
            price_item_edit = request.POST['price_item_edit']
            id_user = request.session.get('id')

            
            item_id_get = Items.objects.filter(id=item_id).first() # витягуватой той товар який обрав користувач
            if item_id_get and item_id_get.author_id_item == id_user: # редагувати товар той який обав користувач і належить користувачу
                item_id_get.name_items = name_item_edit
                item_id_get.description_items = description_item_edit
                item_id_get.category_items = category_items_edit
                item_id_get.phone = phone_user_edit
                item_id_get.price = price_item_edit

                item_id_get.save()


                return redirect('my_profile')
            
            return redirect('my_profile')


    return render(request, 'edit_item.html', context)


def my_orders(request):
    id_user_session = request.session.get('id')
    get_id_order = request.GET.get('get_id_order')

    if not id_user_session:
        return HttpResponse('Увійдіть в кабінет')
    else:
        search_my_orders = Order_Items.objects.filter(id_client=id_user_session)
        if search_my_orders:
            if 'get_id_order' in request.GET:
                get_id_order = request.GET.get('get_id_order')

                return redirect(f'/my_orders-items/{get_id_order}')

            # delete duplicate id sellers
            for id in search_my_orders.values():
                sellers = id['authors_items']
                sellers_conf = id['id_confirmed_sellers']

                list_id_sellers = []
                list_confirmed = []

                for i in sellers:
                    if i not in list_id_sellers:
                        list_id_sellers.append(i)
                
                for x in sellers_conf:
                    if x not in list_confirmed:
                        list_confirmed.append(x)
                
            # all selers and sellers who confirmed order
            count_sellers = len(list_id_sellers)
            cout_confirmed = len(list_confirmed)


            if count_sellers == cout_confirmed:
                update_status_order = search_my_orders.first()

                update_status_order.status_order = 'Підтвердежено'
                update_status_order.save()
                
        not_order_error = '<h1>У вас немає замовлень</h1>'
        if not search_my_orders:
            context = {
                'search_my_orders': search_my_orders.values(),
                'not_order_error': not_order_error,
            }
        else:
            context = {
                'search_my_orders': search_my_orders.values(),
            }

                
    return render(request, 'orders/my_orders.html', context)


def my_orders_items(request, get_id_order):
    id_user_session = request.session.get('id')

    delete_from_order = request.GET.get('delete_from_order')
    my_items_order = Order_Items.objects.filter(id=get_id_order, id_client=id_user_session).values()

    data_order = {
        'list_id_order': [],
        'list_id_items': []
    }

    for i in my_items_order:    
        data_order['list_id_order'].append(i['id'])
        data_order['list_id_items'].append(i['item_id'])

    list_id_order = data_order['list_id_order']
    list_id_items = data_order['list_id_items']                 

    sort_data = {}

    for i in range(len(list_id_order)):
        sort_data[str(list_id_order[i])] = list_id_items[i]

    show_order_item = {}

    for number, item_ids in sort_data.items():  
        info_item = Items.objects.filter(id__in=item_ids).values()
        show_order_item[number] = list(info_item)


    if request.method == 'GET':
        if delete_from_order: 
            order_data_get = Order_Items.objects.get(id=get_id_order)

            list_item_id_order = order_data_get.item_id  
            list_item_id_order.remove(int(delete_from_order))
        
            order_data_get.item_id = list_item_id_order
            order_data_get.save()

            if not order_data_get.item_id:
                order_data_get.delete()

            return redirect('./my_orders/')


    context = {
        'get_id_order': get_id_order,
        'show_order_item': show_order_item,
        'my_items_order': my_items_order
    }

    return render(request, 'orders/my_orders_items.html', context)



def orders_my_client(request):
    id_seller = request.session.get('id')
    if not id_seller:
        return HttpResponse('Увійдіть в кабінет')
    else:
        all_orders = Order_Items.objects.filter(authors_items__icontains=id_seller).values()
        if 'get_id_order' in request.GET:
            get_name_client = request.GET.get('get_name_client')
            get_id_order = request.GET.get('get_id_order')

            return redirect(f'./items-cleint/{get_id_order}/{get_name_client}', get_id_order)        


        #FIXME: Зявляється кнопку при перезавнтажені сторінки
        if 'get_id_order' in request.POST:
            id_order = request.POST.get('get_id_order')
            get_order = Order_Items.objects.filter(authors_items__icontains=id_seller, id=id_order).first()

            get_order.id_confirmed_sellers += [id_seller]
            get_order.save()
            return redirect('.')

        try:
            context = {
                'all_orders': all_orders,
                'get_order': get_order,
                'id_seller': id_seller,
            }
        except UnboundLocalError:     
            context = {
                'all_orders': all_orders,
                'id_seller': id_seller
            }


        return render(request, 'orders/orders_my_client.html', context)


def client_items(request, get_name_client, get_id_order):
    id_seller = request.session.get('id')

    if not id_seller:
        return HttpResponse('Увійдіть в кабінет')
    else:
        all_orders = Order_Items.objects.filter(id=get_id_order, authors_items__icontains=id_seller).values() 

        data_order = {
            'list_id_order': [],
            'list_id_items': []
        }


        for i in all_orders:    
            data_order['list_id_order'].append(i['id'])
            data_order['list_id_items'].append(i['item_id'])


        list_id_order = data_order['list_id_order']
        list_id_items = data_order['list_id_items']                 

        sort_data = {}

        for i in range(len(list_id_order)):
            sort_data[str(list_id_order[i])] = list_id_items[i]

        show_order_item = {}


        for number, item_ids in sort_data.items():  
            info_item = Items.objects.filter(id__in=item_ids, author_id_item=id_seller).values()  
            show_order_item[number] = list(info_item)


        context_client_items = {
            'name_client': get_name_client,
            'show_order_item': show_order_item
        }


    return render(request, 'orders/client_items.html', context_client_items)   