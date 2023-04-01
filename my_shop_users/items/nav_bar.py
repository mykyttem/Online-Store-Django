from django.shortcuts import redirect
import json


def nav_bar_func(request):
    btn_delete_bussket_item = request.GET.get('btn_delete_bussket_item')

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
        value_keys.append(f"""
        <div class="block_shopping_cart" onclick="window.location.href='/items/{i['id_item']}/{i['name_items']}'">
                <h2>{i['name_items']}</h2>
                <h2>{i['price']}</h2>
                <h2>{i['items_info_description']}</h2>

                <h2 style="display:none;">{i['id_item']}</h2>

                <form method="GET">
                    <input type="hidden" name="btn_delete_bussket_item" value="{i['id_item']}">
                    <input type="submit" value="Видалити з корзини">
                </form>

                <hr>
        </div>
        """) 

    save_value_keys = value_keys

    #FIXME НЕ працює ВЗАГАЛІ НІ ДЕ
    if btn_delete_bussket_item: # get button and id_item
        responce = redirect('.')
        new_list = [dictonary for dictonary in json_data
                    if dictonary['id_item'] != int(btn_delete_bussket_item)]

        new_list_dict = {
            "items_bussket": new_list   
        }

        responce.set_cookie('all_item_bussket', json.dumps(new_list_dict))     


        return responce
    

    return {'save_value_keys': save_value_keys}