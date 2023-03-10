from django.shortcuts import render, redirect
from django.template import loader

from .models import Registration
from items.models import Items

from django.http import HttpResponse
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login

from datetime import datetime 


#TODO: ЗРОБИТИ iD ІЗ БІЛЬШЕ ЧИСЛ
#TODO: добавити більше даних для користувача


# Create your views here.
def accounts_users(request):
    if request.method == 'POST':
        login_user = request.POST['login']
        email_user = request.POST['email']
        password_user = request.POST['password']

        # hashed password
        hashed_password = make_password(password_user)


        # search email-dublicate user, from DB
        search_email_dublicate = Registration.objects.filter(
        Q(email_user = f'{email_user}'))

        # search login-dublicate user, from DB
        search_login_dublicate = Registration.objects.filter(
        Q(login_user = f'{login_user}'))



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
        email_user = request.POST['email']
        password_user = request.POST['password']

        # search login user, from DB
        search_login = Registration.objects.filter(
        Q(login_user = f'{login_user}'))


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
    
    myitems = Items.objects.filter(Q(author_id_item=f'{id_user}')).values # витягуєм тільки ті товари, які стоврив користувач
 
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
            item_id_get = Items.objects.filter(Q(id=item_id)).first() # витягуєм тільки ті товари, які стоврив користувач
            if item_id_get and item_id_get.author_id_item == id_user: # видалити товар той який пренадлежит користувачу
                item_id_get.delete()
                
            return redirect('my_profile')


        
        if edit_item:
       
            # print(name_items_get_edit)
            # print(description_get_edit)
            # print(category_get_items_edit)
            # print(phone_get_edit)
            # print(price_get_edit)
            # print(item_id)
            
            return redirect('edit_item')
        




    return render(request, 'my_profile.html', context)



def create_item(request):
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

        
        item_id_get = Items.objects.filter(Q(id=item_id)).first() # витягуватой той товар який обрав користувач
        if item_id_get and item_id_get.author_id_item == id_user: # редагувати товар той який обав користувач і пренадлежит користувачу


            item_id_get.name_items = name_item_edit
            item_id_get.description_items = description_item_edit
            item_id_get.category_items = category_items_edit
            item_id_get.phone = phone_user_edit
            item_id_get.price = price_item_edit

            item_id_get.save()

 

            return redirect('my_profile')
        

        return redirect('my_profile')


    return render(request, 'edit_item.html', context)

