from django.shortcuts import redirect
from .models import Items

import json


def nav_bar_func(request):
    # btn_delete_bussket_item = request.POST.get('btn_delete_bussket_item')

    # get cookies
    get_item_bussket = request.COOKIES.get('all_item_bussket')
    items_bussket_dict = ''

    if get_item_bussket is not None:
        items_bussket_dict = json.loads(get_item_bussket) 

    if items_bussket_dict == '':
        items_bussket_dict = {"items_bussket": []}

    json_data = items_bussket_dict['items_bussket']
    value_keys = []

    
    for i in json_data:
        # added value keys, in list, and buttons in HTML
        value_keys.append(Items.objects.filter(id=i['id_item']).values())
        
    save_value_keys = value_keys
    
    # #FIXME НЕ працює ВЗАГАЛІ НІ ДЕ  
    # if 'btn_delete_basket_item' in request.POST:
    #     btn_delete_bussket_item = request.POST.get('btn_delete_basket_item')
    #     responce = redirect('.')

    #     # new_list = [dictonary for dictonary in json_data
    #     #              if dictonary['id_item'] != int(btn_delete_bussket_item)]

    #     # new_list_dict = {
    #     #      "items_bussket": new_list   
    #     #  }

    #     # responce.set_cookie('all_item_bussket', json.dumps(new_list_dict))     
    #     print("IDD: ", btn_delete_bussket_item)

    #     return responce
        
        

    return {'save_value_keys': save_value_keys}