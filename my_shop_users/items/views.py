from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from django.db.utils import IntegrityError
from django.contrib import messages


from django.db.models import Q
from .models import Items, Items_Reviews

from datetime import datetime 


# Create your views here.
def items(request):
    myitems = Items.objects.all().values
    template = loader.get_template('all_items.html')

    context = {
        'myitems': myitems,
    }


    return HttpResponse(template.render(context, request))



def item_information(request, id, item_name):
    button_reviews = request.POST.get('button_reviews') 

    items_info = Items.objects.filter(Q(id=id) & Q(name_items=item_name)).values() # отримати всю інформацію про елемент, якщо співпадають дані 

    # checking for availability
    search_items = Items.objects.filter(Q(name_items=item_name) & Q(id=id))

    if not search_items:
        return HttpResponse('НЕМАЄ ТАКОГО ТОВАРУ')
    
    else:
        context = {
            'name_items': item_name,
            'items_info': items_info
        }

        if request.method == 'POST':
            if button_reviews:

                return redirect(f'/items/{id}/{item_name}/reviews')


        return render(request, 'item_information.html', context)
    



def reviews_items(request, id, item_name):


    items_info = Items.objects.filter(Q(id=id) & Q(name_items=item_name)).values() # отримати всю інформацію про елемент, якщо співпадають дані 


    if request.method == 'POST':
        # get the item id under which the comment was left
        id_item_review = request.POST.get('id_item_review')
        
    
    # show reviews, only of this item
    see_reviews_this_item = Items_Reviews.objects.filter(id_item_review=id).values() 


    # checking for availability
    search_items = Items.objects.filter(Q(name_items=item_name) & Q(id=id))
    

    if not search_items:
        return HttpResponse('НЕМАЄ ТАКОГО ТОВАРУ')
    else:
        context = {
            'name_items': item_name,
            'items_info': items_info,
            'see_reviews_this_item': see_reviews_this_item

        }   

        try:
            if request.method == 'POST':
                text_review = request.POST['text_review']
                advantages_item = request.POST['advantages_item']
                disadvantages_item = request.POST['disadvantages_item']


                # get session user - id, login
                id_user_review = request.session.get('id')        
                login_user_review = request.session.get('login')


                # check dublicae review person
                check_review_person = Items_Reviews.objects.filter(Q(id_user_review=id_user_review) & Q(id_item_review=id)) # "check id_user_review" and "id_item_review_id"
                if not check_review_person:

                    # date added reiview
                    date_reviews = datetime.now()

                    
                    new_review = Items_Reviews(login_user_review=login_user_review, id_user_review=id_user_review, date_reviews=date_reviews, text_review=text_review, advantages_item=advantages_item, disadvantages_item=disadvantages_item, id_item_review=id_item_review)
                    new_review.save()
                    

                    return redirect(f'/items/{id}/{item_name}/reviews')
                
                else:
                    return HttpResponse('Вже все оставляли свій відгук на цьому товарі')



            
        except IntegrityError:
            messages.success(request, "Щоб залишит відгук, треба увійти в аккунт")
            return redirect(f'/items/{id}/{item_name}/reviews')


    return render(request, 'reviews_items.html', context)