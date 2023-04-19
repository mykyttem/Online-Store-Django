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

        # search login user, from DB
        search_login = Registration.objects.filter(login_user = login_user)

        if not search_login:
            messages.success(request, "Not found account/not correct password")
            return redirect('sign_in')
        else:
            # get user from DB
            user = Registration.objects.get(login_user=login_user)
            # check password
            if check_password(password_user, user.password_user):
                # save session user
                request.session['login'] = user.login_user
                request.session['email'] = user.email_user 
                request.session['id'] = user.id

                return redirect('my_profile')
            else:
                messages.success(request, "Incorrect password")
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
    
    myitems = Items.objects.filter(author_id_item=id_user).values # витягуєм тільки ті товари, які стоврив користувач
 
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
            item_id_get = Items.objects.filter(id=item_id).first() # витягуєм тільки ті товари, які стоврив користувач
            if item_id_get and item_id_get.author_id_item == id_user: # видалити товар той який пренадлежит користувачу
                item_id_get.delete()
                
            return redirect('my_profile')


        if edit_item:            
            return redirect('edit_item')
        

    return render(request, 'my_profile.html', context)



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

    delete_from_order = request.GET.get('delete_from_order')
    get_id_order = request.GET.get('get_id_order')

    if not id_user_session:
        return HttpResponse('Увійдіть в кабінет')
    else:
        search_my_orders = Order_Items.objects.filter(id_client=id_user_session)

        data_order = {
            'list_id_items': [],
            'list_id_order': []
        }

        # get data from my_order, added in dict
        for id in search_my_orders.values():
            id_items = id['item_id']
            id_order = id['id']  
            
            data_order['list_id_order'].append(id_order)        
            data_order['list_id_items'].append(id_items) 


        list_id_order = data_order['list_id_order']
        list_id_items = data_order['list_id_items']
        
        sort_data = {}

        for i in range(len(list_id_order)):
            sort_data[str(list_id_order[i])] = list_id_items[i]


        show_order_item = {}


        for number, item_ids in sort_data.items():  # Отримати ключ та значення (список item_ids) зі словника
            info_item = Items.objects.filter(id__in=item_ids).values()  # Отримати інформацію за значеннями списку item_ids
            show_order_item[number] = list(info_item)


        try:
            context = {
                'info_item': info_item,
                'search_my_orders': search_my_orders.order_by('date_order').values(),
                'show_order_item': show_order_item
            }
        except UnboundLocalError:
            not_order_error = '<h1>У вас немає замовлень</h1>'
            context = {
                'not_order_error': not_order_error,
                'search_my_orders': search_my_orders.order_by('date_order').values(),
                'show_order_item': show_order_item
            }

        #TODO: Добавити видалення товару тільки якщо статус замовлення "Очікування"
        if request.method == 'GET':
            if delete_from_order: 
                order_data_get = Order_Items.objects.get(id=get_id_order)

                list_item_id_order = order_data_get.item_id  
                list_item_id_order.remove(int(delete_from_order))
            
                order_data_get.item_id = list_item_id_order
                order_data_get.save()

                if not order_data_get.item_id:
                    order_data_get.delete()

                return redirect('./my_orders')

                
    return render(request, 'my_orders.html', context)


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
           
            
        context = {
            'all_orders': all_orders
        }


        return render(request, 'orders_my_client.html', context)


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


    return render(request, 'client_items.html', context_client_items)   