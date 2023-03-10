from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.template import loader

from django.db.utils import IntegrityError
from django.contrib import messages

from django.utils.datastructures import MultiValueDictKeyError

from django.db.models import Q
from .models import Items, Items_Reviews, Items_Questions

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
    button_questions = request.POST.get('button_questions')

    # count "reviews" and "questions"
    count_reviews_item = Items_Reviews.objects.filter(id_item_review=id).count() 
    count_questions_item = Items_Questions.objects.filter(id_item_Questions=id).count()


    items_info = Items.objects.filter(Q(id=id) & Q(name_items=item_name)).values() # отримати всю інформацію про елемент, якщо співпадають дані 

    # checking for availability
    search_items = Items.objects.filter(Q(name_items=item_name) & Q(id=id))

    if not search_items:
        return HttpResponse('НЕМАЄ ТАКОГО ТОВАРУ')
    
    else:
        context = {
            'name_items': item_name,
            'items_info': items_info,
            'count_reviews_item': count_reviews_item,
            'count_questions_item': count_questions_item
        }

        if request.method == 'POST':
            if button_reviews:

                return redirect(f'/items/{id}/{item_name}/reviews')
            
            if button_questions:

                return redirect(f'/items/{id}/{item_name}/questions')


        return render(request, 'item_information.html', context)
    



# function reviews for item
def reviews_items(request, id, item_name):
    items_info = Items.objects.filter(Q(id=id) & Q(name_items=item_name)).values() # отримати всю інформацію про елемент, якщо співпадають дані 


    # get session user - id, login
    login_user_review = request.session.get('login')
    id_user_review = request.session.get('id')   


    

    # I could not find a better way to solve the bug when clicking the button
    try:
        if request.method == 'POST':
            text_review = request.POST['text_review']
            advantages_item = request.POST['advantages_item']
            disadvantages_item = request.POST['disadvantages_item']


            # get the item id under which the comment was left
            id_item_review = request.POST.get('id_item_review')


            try:
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
            
            

    except MultiValueDictKeyError:
        # fields edit
        text_review_edit = request.POST['text_review_edit']
        advantages_item_edit = request.POST['advantages_item_edit']
        disadvantages_item_edit = request.POST['disadvantages_item_edit']


        # button Delete, my review
        delete_my_review = request.POST.get('delete_my_review')


        # activate button - delete my review
        if delete_my_review:
            # find my review

            find_my_review_this_item = Items_Reviews.objects.filter(Q(id_user_review=id_user_review) & Q(id_item_review=id)) # "check id_user_review" and "id_item_review_id"
            find_my_review_this_item.delete()


        # edit my review
        if request.method == 'POST':
            get_my_review = Items_Reviews.objects.filter(Q(id_user_review=id_user_review) & Q(id_item_review=id)).first() # "check id_user_review" and "id_item_review_id"

            if get_my_review:
                get_my_review.text_review = text_review_edit
                get_my_review.advantages_item = advantages_item_edit
                get_my_review.disadvantages_item = disadvantages_item_edit

                get_my_review.save()   
                



    # show reviews, only of this item
    see_reviews_this_item = Items_Reviews.objects.filter(id_item_review=id).values() 


    # checking for availability
    search_items = Items.objects.filter(Q(name_items=item_name) & Q(id=id))
    

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











# function questions for item
def questions_items(request, id, item_name):

    items_info = Items.objects.filter(Q(id=id) & Q(name_items=item_name)).values() # отримати всю інформацію про елемент, якщо співпадають дані 


    # get session user - id, login
    login_user_Questions = request.session.get('login')
    id_user_Questions = request.session.get('id')   



    # I could not find a better way to solve the bug when clicking the button
    try:
        if request.method == 'POST':
            text_Questions = request.POST['text_Questions']


            # get the item id under which the comment was left
            id_item_Questions = request.POST.get('id_item_Questions')


            try:
                # check dublicae Questions person
                check_Questions_person = Items_Questions.objects.filter(Q(id_user_Questions=id_user_Questions) & Q(id_item_Questions=id)) # "check id_user_Questions" and "id_item_Questions_id"
                if not check_Questions_person:

                    # date added Questions
                    date_Questions = datetime.now()

                    new_Questions = Items_Questions(login_user_Questions=login_user_Questions, id_user_Questions=id_user_Questions, date_Questions=date_Questions, text_Questions=text_Questions, id_item_Questions=id_item_Questions)
                    new_Questions.save()
                    

                    return redirect(f'/items/{id}/{item_name}/questions')
                
                else:
                    return HttpResponse('Вже все оставляли своє питання на цьому товарі')
                
            except IntegrityError:
                messages.success(request, "Щоб залишит відгук, треба увійти в аккунт")
                return redirect(f'/items/{id}/{item_name}/questions')
            
            

    except MultiValueDictKeyError:
        # fields edit questions
        text_Questions_edit = request.POST['text_Questions_edit']


        # button Delete, and edit my Questions
        delete_my_Questions = request.POST.get('delete_my_Questions')



        # activate button - delete my Questions
        if delete_my_Questions:
            # find my Questions
            find_my_Questions_this_item = Items_Questions.objects.filter(Q(id_user_Questions=id_user_Questions) & Q(id_item_Questions=id)) # "check id_user_Questions" and "id_item_Qustions_id"
            find_my_Questions_this_item.delete()


        # edit my Questions
        if request.method == 'POST':
            get_my_Questions = Items_Questions.objects.filter(Q(id_user_Questions=id_user_Questions) & Q(id_item_Questions=id)).first() # "check id_user_Question" and "id_item_review_Questio"

            if get_my_Questions:
                get_my_Questions.text_Questions = text_Questions_edit


                get_my_Questions.save()   
                
            
        


        


    # show Questions, only of this item
    see_Questions_this_item = Items_Questions.objects.filter(id_item_Questions=id).values() 


    # checking for availability
    search_items = Items.objects.filter(Q(name_items=item_name) & Q(id=id))
    

    # show my Questions
    show_my_Questions = Items_Questions.objects.filter(id_user_Questions=id_user_Questions, id_item_Questions=id).values() 

    

    if not search_items:
        return HttpResponse('НЕМАЄ ТАКОГО ТОВАРУ')
    else:
        context = {
            'name_items': item_name,
            'items_info': items_info,
            'see_Questions_this_item': see_Questions_this_item,
            'show_my_Questions': show_my_Questions
        }   


        
    return render(request, 'questions_items.html', context)


