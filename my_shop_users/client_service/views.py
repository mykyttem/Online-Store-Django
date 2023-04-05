"""
Файл буде відповідати за обслогоування клієнта, наприклад: оформити замовлення, тех-підтримка.
"""
from django.shortcuts import render, redirect
from .models import Order_Items

# оформлення замовлення
def checkout(request):
    # data checkout
    if request.method == 'POST': 
        #TODO: коли ставиться одна галочка, то повина прибиратися інша

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

        
        save_order = Order_Items(client_number=client_number, client_name=client_name, client_username=client_username, client_email=client_email, 
                    payment_upon_receipt=payment_upon_receipt, online_payment=online_payment, I_receiver=I_receiver, other_person=other_person, do_not_call_me_back=do_not_call_me_back, author_item_id=0)
        save_order.save()
    

        return redirect('./checkout')
        

    context = {
        'test': 'test'
    }


    return render(request, 'checkout.html', context)