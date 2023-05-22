from django.shortcuts import render, redirect
from django.db.models import Q

from accounts_users.models import Registration
from .models import Order_Items, Chat_UserSeller, MessageChat
from items.models import Items

from django.contrib import messages

import json
from datetime import datetime


# placing an order
def checkout(request):
    id_purchaser_session = request.session.get('id')    
    get_item_bussket = request.COOKIES.get('all_item_bussket')

    if not id_purchaser_session:
        return redirect('sign_in')
    elif not get_item_bussket:
        messages.success('В кошику нічого немає =(')
        return redirect('.')
    else:   
        search_my_orders = Order_Items.objects.filter(id_client=id_purchaser_session).values()

        # get cookies
        items_bussket_dict = json.loads(get_item_bussket) 

        # get id items from cookies
        json_data = items_bussket_dict['items_bussket']
        order_amount = sum([i['price'] for i in json_data])

        list_id_items = []
        list_author_items = []

        for dictonary in json_data:
            list_id_items.append(dictonary['id_item'])
            get_author_id_item = Items.objects.filter(id=dictonary['id_item']).values()
            
            for id_author in get_author_id_item:
                list_author_items.append(id_author['author_id_item'])

        
        # get item from order
        items_id_order = []
        for id in search_my_orders:
            items_id_order.append(id['item_id'])


        # data checkout
        if request.method == 'POST': 
            # Contact Information
            client_number = request.POST['your_number']
            client_name = request.POST['your_name']
            client_username = request.POST['your_surname']
            client_email = request.POST['your_email']

            # Payment
            payment_upon_receipt = request.POST.get('payment_upon_receipt') 
            online_payment = request.POST.get('online_payment') 

            # Recipient
            I_receiver = request.POST.get('I_receiver')  
            other_person = request.POST.get('other_person') 
            do_not_call_me_back = request.POST.get('do_not_call_me_back')

            # promotion_code
            promotion_code = request.POST.get('type_promotion_code') 

            # find code in Items
            if not promotion_code:
                find_promotion_code = Items.objects.filter(id__in=list_id_items)
            else:
                find_promotion_code = Items.objects.filter(promotion_code=promotion_code, id__in=list_id_items)

                # formating date
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                if find_promotion_code.exists():
                    validity_period_promocode_str = find_promotion_code.first().validity_period_promocode.strftime("%Y-%m-%d %H:%M:%S.%f")
            

                if not find_promotion_code.exists():
                    messages.error(request, "Промокод не вірний")
                    return redirect('.')


                # checked date and typing code  
                if 0 == find_promotion_code.first().amount_type_promotion_code or datetime.strptime(validity_period_promocode_str, "%Y-%m-%d %H:%M:%S.%f") < datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S.%f"):
                    messages.error(request, "Промокод більше не активний")
                    return redirect('.')
                            
                        
                elif id_purchaser_session in find_promotion_code.first().purchaser_type_code:
                    messages.error(request, "Ви вже використали цей промокод")
                    return redirect('.')

            
            # discount percentage    
            order_amount = sum([i['price'] for i in json_data])
                
            for i in find_promotion_code.values():
                new_order_amount = order_amount - i['at_what_price'] if i['at_what_price'] is not None else order_amount
                discount = ((order_amount - new_order_amount) / order_amount) * 100

                # reducing available activations
                find_promotion_code = find_promotion_code.first()
                if find_promotion_code:
                    if find_promotion_code.amount_type_promotion_code is not None:
                        find_promotion_code.amount_type_promotion_code -= 1
                        find_promotion_code.purchaser_type_code.append(id_purchaser_session)
                        find_promotion_code.save()


                # save data     
                if 'on' == payment_upon_receipt:
                    payment_upon_receipt = True 
                else:
                    payment_upon_receipt = False

                if 'on' == online_payment:
                    online_payment = True
                else:
                    online_payment = False

                if 'on' == I_receiver:
                    I_receiver = True
                else:
                    I_receiver = False

                if 'on' == other_person:
                    other_person = True
                else:
                    other_person = False

                if 'on' == do_not_call_me_back:
                    do_not_call_me_back = True
                else:
                    do_not_call_me_back = False


                date_time_now = datetime.now()

                save_order = Order_Items(client_number=client_number, client_name=client_name, client_username=client_username, client_email=client_email, 
                            payment_upon_receipt=payment_upon_receipt, online_payment=online_payment, I_receiver=I_receiver, other_person=other_person, 
                            do_not_call_me_back=do_not_call_me_back, item_id=list_id_items, authors_items=list_author_items, id_client=id_purchaser_session, 
                            date_order=date_time_now, order_amount=None if order_amount == '' else order_amount, order_amount_use_promotion_code=None if new_order_amount == '' else new_order_amount , discount=None if discount == '' else discount)
                save_order.save()
                            

                response = redirect('my_orders')
                response.delete_cookie('all_item_bussket')

                return response


    context = {
        'json_data': json_data,
        'all_sum_items': order_amount
    }
        

    return render(request, 'checkout.html', context)


def room(request, room_name):
    id_user = request.session.get('id')

    if not id_user:
        return redirect('/items')    


    # get data from url 
    get_channels = Chat_UserSeller.objects.filter(name_channel=room_name).values()
    get_messages_channels = MessageChat.objects.filter(chat=room_name).values()
    
    id_seller = room_name.replace('_', ' ').split()[1]
    id_buyer = room_name.replace('_', ' ').split()[3]


    # checking if user is a member of the chat
    if (id_user == int(id_buyer)) or (id_user == int(id_seller)):

        # checking person in chat
        if not id_user == int(id_buyer):
            search_interlocutor = Registration.objects.filter(id=id_buyer).values()
        else:
            search_interlocutor = Registration.objects.filter(id=id_seller).values()
            
    
        if not get_channels:

            # save room     
            Chat_UserSell = Chat_UserSeller(name_channel=room_name, id_buyer=id_buyer, id_seller=id_seller)
            Chat_UserSell.save()
        

        chats = Chat_UserSeller.objects.filter(Q(id_buyer=id_user) | Q(id_seller=id_user)).values()  
        search_list_chat = Registration.objects.all()  
        
        
        context =  {
            'room_name': room_name,
            'messages': get_messages_channels,
            'name_interlocutor': search_interlocutor,
            'id_user': id_user,
            'chats': chats,
            'interlocutor': search_list_chat, 
        }

    else:
        return redirect('/items')


    return render(request, "channel_chat.html", context)