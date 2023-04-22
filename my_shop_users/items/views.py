from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

from .models import Items, Items_Reviews, Items_Questions, Items_Questions_Replys
from accounts_users.models import Registration

from datetime import datetime 
import json


def items(request):
    myitems = Items.objects.all().values()

    if 'search_item_field' in request.POST:
        search_item_field = request.POST.get('search_item_field')  
        all_items_name_search = Items.objects.filter(name_items__icontains=search_item_field).first()
        
        if not all_items_name_search:
            return render(request, 'error_pages/not_found_item.html', {'not_found_item': search_item_field})
        else:
            return redirect(f'search_item/{search_item_field}', search_item_field)
         
    context = {
        'myitems': myitems # all items
    }

    return render(request, 'all_items.html', context)


#TODO: зробити кнопку очистити фільтри
#TODO: зробити ліміт на блоків в одну сторінку, щоб було наприклад: items/page1 or items/page2
#TODO: добавити інші фільтри
#FIXME: не завжди зявляється при пошуку(більше повязано з кнопками)
def item_search(request, result_item_name):
    """ 
    На сторінці пошуку, зявляються результат пошуку, кнопки, сортуваня, фільтри.
    """
    all_items_search = Items.objects.filter(name_items__icontains=result_item_name).values()

    # fix bug, local variable    
    items_cheap_to_expencive, items_expencive_to_cheap, new_ones_first, reviews_result, filter_price = [], [], [], [], []


    if request.method == 'POST':
        # filters price
        first_price = request.POST['first_price']
        last_price = request.POST['last_price']

        # apply price filter
        filter_price = Items.objects.filter(name_items__icontains=result_item_name, price__gte=first_price, price__lte=last_price).values()
        

    if request.method == 'GET':
        # buttons - від дешевих до дорогих, від дорого до дешевого, New items, Reviews
        sort_cheap_to_expensive = request.GET.get('sort_cheap_to_expensive', "") 
        sort_expensive_tp_cheap = request.GET.get('sort_expensive_to_cheap', "") 
        new_item = request.GET.get('newItem', "") 
        more_review = request.GET.get('more_review', "")
        

        if sort_cheap_to_expensive: 
            items_cheap_to_expencive = Items.objects.filter(name_items__icontains=result_item_name).order_by('price').values() 
        if sort_expensive_tp_cheap:
            items_expencive_to_cheap = Items.objects.filter(name_items__icontains=result_item_name).order_by('-price').values()
        if new_item:
            new_ones_first = Items.objects.filter(name_items__icontains=result_item_name).order_by('-id').values()
        if more_review:
            reviews = Items.objects.filter(name_items__icontains=result_item_name).values_list('id', flat=True) # search id this item
            review_find = Items_Reviews.objects.filter(id_item_review__in=reviews).values_list('id_item_review', flat=True) # search id_review this item
            reviews_result = Items.objects.filter(id__in=review_find).values() # get item this review 
            
    
    context_result_search = {
        'all_items_search': all_items_search,
        'search_item_field': result_item_name,

        # sorting
        'items_cheap_to_expencive': items_cheap_to_expencive,
        'items_expencive_to_cheap': items_expencive_to_cheap,
        'new_ones_first': new_ones_first,
        'reviews_result': reviews_result,

        # filters
        'filter_price': filter_price
    }


    return render(request, 'get_result_search.html', context_result_search)


#TODO: поставити шифр/захист на cookie 
#TODO: зробити, скільки потрібно замовити товару (наприклад: playstation 1, 2, 3) - і ціна змінюється
def item_information(request, id, item_name):
    """Інформації о товарі, можно переглянути відгуки, та питання до товару, добавити в коризну"""
    responce = redirect('.')

    button_reviews = request.GET.get('button_reviews') 
    button_questions = request.GET.get('button_questions')
    button_shoping_basket = request.GET.get('btn_shoping_basket')
    
    # btn_delete_bussket_item = request.GET.get('btn_delete_bussket_item')

    # count "reviews" and "questions"
    count_reviews_item = Items_Reviews.objects.filter(id_item_review=id).count() 
    count_questions_item = Items_Questions.objects.filter(id_item_Questions=id).count()
 
    # Get All Info for item
    items_info = Items.objects.get(id=id, name_items=item_name) 
    items_info_price = items_info.price 
    items_info_description = items_info.description_items   

    # get seller this item
    get_seller = Registration.objects.filter(id=items_info.author_id_item).values()

    # checking for availability
    search_items = Items.objects.filter(name_items=item_name, id=id)

    #  get cookies
    get_item_bussket = request.COOKIES.get('all_item_bussket')
    items_bussket_dict = ''

    if get_item_bussket is not None:
        items_bussket_dict = json.loads(get_item_bussket) 


    if items_bussket_dict == '':
        items_bussket_dict = {"items_bussket": []}


    json_data = items_bussket_dict['items_bussket']

    checking_item_in_bussket = [dictonary for dictonary in json_data
                    if dictonary['id_item'] == id]
    
    
    if not search_items:
        return render(request, 'error_pages/not_found_item.html', {'not_found_item': search_items})    
    else:        
        context = {
            # info for item
            'name_items': item_name,
            'items_info_price': items_info_price,
            'items_info_description': items_info_description,

            'get_seller': get_seller,
            
            # count 
            'count_reviews_item': count_reviews_item,
            'count_questions_item': count_questions_item,

            'checking_item_in_bussket': checking_item_in_bussket
        }

        
        if request.method == 'GET':
            if button_reviews:
                return redirect(f'/items/{id}/{item_name}/reviews')
                        
            if button_questions:
                return redirect(f'/items/{id}/{item_name}/questions')
            
            if button_shoping_basket:
                items_bussket_dict["items_bussket"].append(
                    {"name_items": item_name,
                    "price": items_info_price,
                    "items_info_description": items_info_description,
                    "id_item": id}
                )
                responce.set_cookie('all_item_bussket', json.dumps(items_bussket_dict))    

                return responce

        
        return render(request, 'item_information.html', context)

    
def reviews_items(request, id, item_name):
    items_info = Items.objects.filter(id=id, name_items=item_name).values()

    # get session user - id, login
    login_user_review = request.session.get('login')
    id_user_review = request.session.get('id')   

    # get the item id under which the comment was left
    id_item_review = request.POST.get('id_item_review')
    delete_my_review = request.POST.get('delete_my_review')

    useful_review = request.GET.get('btn_useful_review')
    not_useful_review = request.GET.get('btn_not_useful_review')


    if 'text_review' in request.POST:
        text_review = request.POST['text_review']
        advantages_item = request.POST['advantages_item']
        disadvantages_item = request.POST['disadvantages_item']


        if not login_user_review:
            messages.success(request, "Щоб залишит відгук, треба увійти в аккунт")
            return redirect(f'/items/{id}/{item_name}/reviews')
        else:
            # check dublicate review person
            check_review_person = Items_Reviews.objects.filter(id_user_review=id_user_review, id_item_review=id) 
            if not check_review_person:
                # date added review
                date_reviews = datetime.now()

                new_review = Items_Reviews(login_user_review=login_user_review, id_user_review=id_user_review, 
                                           date_reviews=date_reviews, text_review=text_review, 
                                           advantages_item=advantages_item, disadvantages_item=disadvantages_item, id_item_review=id_item_review)
                new_review.save()
                
                return redirect(f'/items/{id}/{item_name}/reviews')
            else:
                return HttpResponse('Вже все оставляли свій відгук на цьому товарі')
            
    # find my review
    find_my_review_this_item = Items_Reviews.objects.filter(id_user_review=id_user_review,  id_item_review=id)

    # activate button - delete my review
    if delete_my_review:
        find_my_review_this_item.delete()

    
    if useful_review:
        review = Items_Reviews.objects.filter(id=useful_review).first()

        if id_user_review in review.count_useful_review:
            review.count_useful_review.remove(id_user_review)
        else:
            review.count_useful_review.append(id_user_review)

        review.save()
        return redirect('./reviews')
    

    if not_useful_review:
        review = Items_Reviews.objects.filter(id=not_useful_review).first()

        if id_user_review in review.count_not_useful_review:
            review.count_not_useful_review.remove(id_user_review)
        else:
            review.count_not_useful_review.append(id_user_review)

        review.save()
        return redirect('./reviews')
        

    if 'text_review_edit' in request.POST:
        # fields edit, advantages, disadvantages, delete
        text_review_edit = request.POST['text_review_edit']
        advantages_item_edit = request.POST['advantages_item_edit']
        disadvantages_item_edit = request.POST['disadvantages_item_edit']

        # edit my review   
        get_my_review = find_my_review_this_item.first() # "check id_user_review" and "id_item_review_id"

        if get_my_review:
            get_my_review.text_review = text_review_edit
            get_my_review.advantages_item = advantages_item_edit
            get_my_review.disadvantages_item = disadvantages_item_edit

            get_my_review.save()   
                

    # show reviews, only of this item
    see_reviews_this_item = Items_Reviews.objects.filter(id_item_review=id).values() 

    # checking for availability
    search_items = Items.objects.filter(name_items=item_name, id=id)
    
    # show my reviews
    show_my_review = Items_Reviews.objects.filter(id_user_review=id_user_review, id_item_review=id).values() 

    if not search_items:
        return HttpResponse('НЕМАЄ ТАКОГО ТОВАРУ')
    else:
        context = {
            'name_items': item_name,
            'items_info': items_info,
            'see_reviews_this_item': see_reviews_this_item,
            'show_my_review': show_my_review
        }   

    return render(request, 'reviews_items.html', context)


def questions_items(request, id, item_name):
    items_info = Items.objects.filter(id=id, name_items=item_name).values()

    # get session user - id, login
    login_user_Questions = request.session.get('login')
    id_user_Questions = request.session.get('id')  
     

    # get the item id under which the comment was left
    id_item_Questions = request.POST.get('id_item_Questions')
    delete_my_Questions = request.POST.get('delete_my_Questions')


    useful_question = request.GET.get('btn_useful_question')
    not_useful_question = request.GET.get('btn_not_useful_question')

    useful_question_reply = request.GET.get('btn_useful_question_reply')
    not_useful_question_reply = request.GET.get('btn_not_useful_question_reply')


    if 'text_Questions' in request.POST:
        text_Questions = request.POST['text_Questions']

        if not login_user_Questions:
            messages.success(request, "Щоб залишит відгук, треба увійти в аккунт")
            return redirect(f'/items/{id}/{item_name}/questions')
        else:
            # check dublicate Questions person
            check_Questions_person = Items_Questions.objects.filter(id_user_Questions=id_user_Questions, id_item_Questions=id) # "check id_user_Questions" and "id_item_Questions_id"
            if not check_Questions_person:
                date_Questions = datetime.now()

                new_Questions = Items_Questions(login_user_Questions=login_user_Questions, id_user_Questions=id_user_Questions, date_Questions=date_Questions, text_Questions=text_Questions, id_item_Questions=id_item_Questions)
                new_Questions.save()
                
                return redirect(f'/items/{id}/{item_name}/questions')
            else:
                return HttpResponse('Вже все оставляли своє питання на цьому товарі')
               

    find_my_Questions_this_item = Items_Questions.objects.filter(id_user_Questions=id_user_Questions, id_item_Questions=id) # "check id_user_Questions" and "id_item_Qustions_id"

    # activate button - delete my Questions
    if delete_my_Questions:
        find_my_Questions_this_item.delete()

    
    if useful_question:
        get_data_question = Items_Questions.objects.filter(id=useful_question).first()

        if id_user_Questions in get_data_question.count_useful_Questions:
            get_data_question.count_useful_Questions.remove(id_user_Questions)
        else:
            get_data_question.count_useful_Questions.append(id_user_Questions)
          
        get_data_question.save()
        return redirect('./questions')


    if not_useful_question:
        get_data_question = Items_Questions.objects.filter(id=not_useful_question).first()
        
        if id_user_Questions in get_data_question.count_not_useful_Questions:
            get_data_question.count_not_useful_Questions.remove(id_user_Questions)
        else:
            get_data_question.count_not_useful_Questions.append(id_user_Questions)
            

        get_data_question.save()
        return redirect('./questions')
        
        
    if useful_question_reply:
        get_data_question_reply = Items_Questions_Replys.objects.filter(id=useful_question_reply).first()

        if id_user_Questions in get_data_question_reply.count_useful_Questions_reply:
            get_data_question_reply.count_useful_Questions_reply.remove(id_user_Questions)
        else:
            get_data_question_reply.count_useful_Questions_reply.append(id_user_Questions)

        get_data_question_reply.save()
        return redirect('./questions')
        
    
    if not_useful_question_reply:
        get_data_question_reply = Items_Questions_Replys.objects.filter(id=not_useful_question_reply).first()

        if id_item_Questions in get_data_question_reply.count_not_useful_Questions_reply:
            get_data_question_reply.count_not_useful_Questions_reply.remove(id_user_Questions)
        else:
            get_data_question_reply.count_not_useful_Questions_reply.append(id_user_Questions)

        get_data_question_reply.save()
        return redirect('./questions')


    if 'text_Questions_edit' in request.POST:
        text_Questions_edit = request.POST['text_Questions_edit']

        # edit my Questions
        get_my_Questions = find_my_Questions_this_item.first() # "check id_user_Question" and "id_item_review_Questio"
        if get_my_Questions:
            get_my_Questions.text_Questions = text_Questions_edit
            get_my_Questions.save() 


    delete_my_reply = request.GET.get('delete_my_reply')
    if 'reply_id_quest' in request.POST:        
        reply_text = request.POST.get('reply_text')
        reply_id_quest = request.POST['reply_id_quest']

        # reply 
        date_reply = datetime.now()

        save_reply = Items_Questions_Replys(login_user_Questions_reply=login_user_Questions, id_user_Questions_reply=id_user_Questions, id_item_Questions_reply=reply_id_quest, date_Questions_reply=date_reply, text_Questions_reply=reply_text)
        save_reply.save()
        return redirect('./questions')
    

    my_id_reply = delete_my_reply
    find_my_reply = Items_Questions_Replys.objects.filter(id_user_Questions_reply=id_user_Questions, id=my_id_reply)
    if delete_my_reply:
        find_my_reply.delete()


    if 'reply_text_edit' in request.POST:
        reply_id_quest_edit = request.POST.get('reply_id_quest_edit')
        reply_text_edit = request.POST['reply_text_edit']
        
        get_my_reply = Items_Questions_Replys.objects.filter(id_user_Questions_reply=id_user_Questions, id=reply_id_quest_edit).first()
        
        get_my_reply.text_Questions_reply = reply_text_edit
        get_my_reply.save(update_fields=['text_Questions_reply']) 


    # show my Questions, and other Questions, only of this item
    see_Questionss_this_item = Items_Questions.objects.filter(id_item_Questions=id).values() 
    show_my_Questions = Items_Questions.objects.filter(id_user_Questions=id_user_Questions, id_item_Questions=id).values() 


    # Show reply
    see_reply_this_item = Items_Questions_Replys.objects.values()
    see_my_reply = Items_Questions_Replys.objects.filter(id_user_Questions_reply=id_user_Questions).values


    # checking for availability
    search_items = Items.objects.filter(name_items=item_name, id=id)
    

    if not search_items:
        return HttpResponse('НЕМАЄ ТАКОГО ТОВАРУ')
    else:
        context = {
            'name_items': item_name,
            'items_info': items_info,
            'id_user_Questions': id_user_Questions,

            'see_Questionss_this_item': see_Questionss_this_item,
            'show_my_Questions': show_my_Questions,

            'see_reply_this_item': see_reply_this_item,
            'see_my_reply': see_my_reply    
        }   


    return render(request, 'questions_items.html', context)