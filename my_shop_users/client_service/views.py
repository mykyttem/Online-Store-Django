"""
Файл буде відповідати за обслогоування клієнта, наприклад: оформити замовлення, тех-підтримка.
"""
from django.shortcuts import render, redirect, HttpResponse
from .models import Order_Items
from items.models import Items

import json
from datetime import datetime

#FIXME: прибрати кнопки з товарів на цій сторінці
#FIXME: кнопка реагує тільки на клавішу "enter" - повязано з тим що на сторінці після цього кнопки на товараї - треба прибрати
#FIXME: сломались кнопки з галочками - в БД не немає 1 або 0 (причина що і ☝)
#FIXME: коли ставиться одна галочка, то повина прибиратися інша

# оформлення замовлення
def checkout(request):
    id_user_session = request.session.get('id')    
    search_my_orders = Order_Items.objects.filter(id_client=id_user_session).values()

    # get cookies
    get_item_bussket = request.COOKIES.get('all_item_bussket')
    items_bussket_dict = json.loads(get_item_bussket) 

    # get id items from cookies
    json_data = items_bussket_dict['items_bussket']
    list_id_items = []

    for dictonary in json_data:
        list_id_items.append(dictonary['id_item'])
    
    # get item from order
    items_id_order = []
    for id in search_my_orders:
        items_id_order.append(id['item_id'])


    # data checkout
    if request.method == 'POST': 
        for value in list_id_items:
            # Search item on id
            search_item_id = Items.objects.filter(id=str(value).replace('[', '').replace(']', '')).values()
            for name in search_item_id:
                name_item = name['name_items']

            if not id_user_session:
                return HttpResponse('Щоб оформити товар, потрібно увійти в акаунт або зарегеструватися')       
            elif value in list_id_items:
                return HttpResponse(f'Товар "{name_item}" вже є в замовленях')
            else:
                # Контактна інформація
                client_number = request.POST['your_number']
                client_name = request.POST['your_name']
                client_username = request.POST['your_surname']
                client_email = request.POST['your_email']

                # Оплата
                payment_upon_receipt = request.POST.get('payment_upon_receipt') 
                online_payment = request.POST.get('online_payment') 

                # Отримувач
                I_receiver = request.POST.get('I_receiver')  
                other_person = request.POST.get('other_person') 
                do_not_call_me_back = request.POST.get('do_not_call_me_back')

                
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
                            payment_upon_receipt=payment_upon_receipt, online_payment=online_payment, I_receiver=I_receiver, other_person=other_person, do_not_call_me_back=do_not_call_me_back, item_id=list_id_items, id_client=id_user_session, date_order=date_time_now)
                save_order.save()
        
                # delete items from bussket
                response = redirect('./my_orders')
                response.delete_cookie('all_item_bussket')


                return response
                

    return render(request, 'checkout.html')