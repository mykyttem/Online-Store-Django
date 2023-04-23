from django.shortcuts import render, redirect

from items.models import Items
from client_service.models import Order_Items

from django.http import HttpResponse


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