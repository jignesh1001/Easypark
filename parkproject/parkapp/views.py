from django.shortcuts import render,redirect, resolve_url
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as dj_login,logout
from django.contrib.auth.decorators import login_required
from parkapp.forms import TYPEForm,OWNERForm,CUSTOMERForm,BOOKForm
from parkapp.models import TYPER
from django.http import HttpResponse
from parkapp.models import OWNER,CUSTOMER,BOOK

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/main')
    return render(request,'index.html')

    
# ####changing
def about(request):
    return render(request,'about.html')
def contactUs(request):
    return render(request,'contact_us.html')

    #######

###
def login(request):
     if request.method == 'GET':
        return render(request,'login.html')
     else :
        loginusername = request.POST.get('loginuser')
        loginpassword = request.POST.get('loginpassword')

        user= authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            dj_login(request,user)
            return redirect('/main')
        else:
            return HttpResponse('Your Credentials are wrong,please try again!')
            # return messages.success(request,"Request Sent , Please Wait for response")
            # return redirect('/login')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        name = request.POST.get('user')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        # Check if username already exists
        if User.objects.filter(username=name).exists():
            messages.error(request, 'This Username already exists. Choose a different username')
            return render(request, 'signup.html')
        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')
        # Create user
        myuser = User.objects.create_user(username=name, email=email, password=pass1)
        myuser.save()
        # Log in the user
        user = authenticate(username=name, password=pass1)
        if user is not None:
            dj_login(request, user)
            return redirect('/usertype')
        else:
            # This should not happen, but just in case
            messages.error(request, 'Unable to log in, please try again.')
            return render(request, 'signup.html')

@login_required(login_url='/login')
def main(request):
    flag = 'F'
    b_flag = 'F'
    for item in CUSTOMER.objects.all():
        if item.user==request.user:
            flag='T'
            break

    for book in BOOK.objects.all():
        if book.owner == request.user.username:
            b_flag = 'T'
            break

    acceptor = ''
    searchtext = ''
    
    if request.method=='GET':
        allowners = ''
        selfspots = ''
        allcustomers = ''
        notaval = ''
        if request.user.is_authenticated:
            oform = OWNERForm()
            user = request.user
            utype = TYPER.objects.filter(user=user)

            # for cards
            if flag == 'T':
                if 'q' in request.GET:
                    q=request.GET['q']
                    allowners=OWNER.objects.filter(city__icontains=q)
                    for o in allowners:
                        if str(o.city):
                            searchtext = "Results related to your search are as follows"
                        else:
                            searchtext = "No slots in searched city"
                        break
                else:
                    allowners=OWNER.objects.all().exclude(no_of_slots=0)
                    notaval=OWNER.objects.filter(no_of_slots = 0)



            # For Booking Cards
            if b_flag == 'T':
                allcustomers = BOOK.objects.filter(owner = request.user.username,bool_value=False)
                allconcustomers = BOOK.objects.filter(owner = request.user.username,bool_value=True)
            


            # for owner cards
            selfspots = OWNER.objects.filter(name = request.user.username)

            #For Booked Customers
            booked_customers = BOOK.objects.filter(bool_value=True,customer=request.user.username)
                


            return render(request,'main.html',context={'type':utype,'oform':oform,'flag':flag,'allowners':allowners,'selfspots':selfspots,'b_flag':b_flag,'allcustomers':allcustomers,'acceptor':booked_customers,'allconcustomers':allconcustomers,'searchtext':searchtext,'notaval':notaval})
        else:
            return render(request,'main.html')
    else:
        return redirect('/addinfo')


def addinfo(request):
    info = request.POST
    name = request.user.username
    no_of_slots = info.get('no_of_slots')
    phone_number=info.get('phone')
    city=info.get('city')
    address=info.get('address')
    prices=info.get('prices')
    if name == "" or phone_number=="" or city=="" or address=="" or prices == "":
        messages.error(request,'no fields can be empty')
    else:
        owner = OWNER(name=name,phone_number=phone_number,city=city,address=address,no_of_slots=no_of_slots, prices=prices)
        owner.save()
    return redirect('/main')

def userlogout(request):
    logout(request)
    return redirect('/')

def usertype(request):
    if request.method=='GET':
        form = TYPEForm()
        return render(request,'usertype.html',context={'form':form})
    else:
        form = TYPEForm(request.POST)
        if form.is_valid():
            user = request.user
            utype = form.save(commit=False)
            utype.user = user
            utype.save()
        return redirect('/main')

def crepro(request):
    if request.method == 'GET':
        form = CUSTOMERForm()
        return render(request,'crepro.html',context={'form':form})
    else:
        form = CUSTOMERForm(request.POST)
        if form.is_valid(): 
            info = form.save(commit=False)
            info.user = request.user
            info.save()
            return redirect('/main')
        return HttpResponse('Invalid data , please fill carefully')


def check_profile(request):
    user = request.user
    data = CUSTOMER.objects.filter(user=user)
    return render(request,'check_profile.html',context={'data':data})

def delete_spot(request,id):
    del_id = id
    OWNER.objects.get(id=del_id).delete()
    return redirect('/main')

def book_spot(request,id):

    if request.method == 'GET':
        all_obj = BOOK.objects.filter(key_num = id)
        for obj in all_obj:
            a = obj.customer
            b = request.user.username
            if a == b:
                messages.error(request,"Can't book the same slot again")
                return redirect('/main')
        bookform = BOOKForm()
        book_id = id
        owner = OWNER.objects.get(id=book_id)

        customer = request.user.username
        return render(request,'book.html',context={'bookform':bookform,'book_owner':owner,'book_customer':customer})
    else:
        form = BOOKForm(request.POST)
        book_id = id
        owner = OWNER.objects.get(id=book_id)
        if form.is_valid():
            book_obj = form.save(commit=False)
            book_id = id
            book_obj.owner = owner.name
            book_obj.spot = owner.address
            book_obj.customer = request.user.username
            book_obj.key_num = book_id
            

            book_obj.save()
            messages.success(request,"Request Sent , Please Wait for response")
            return redirect('/main')

def accept(request,id):
    bingo = BOOK.objects.get(key_num=id)
    bingo.bool_value = True
    bingo.save()
    owner = bingo.owner
    address = bingo.spot
    owner_data = OWNER.objects.get(name=owner,address=address)
    owner_data.no_of_slots = owner_data.no_of_slots-1
    owner_data.save()
    messages.success(request,'Slot acepteted sucessfully')
    return redirect('/main')

def decline(request,id):
    BOOK.objects.get(key_num=id).delete()
    messages.success(request,'Offer Declined')
    return redirect('/main')

def free_slot(request,id):
    owner = BOOK.objects.get(key_num=id).owner
    address = BOOK.objects.get(key_num=id).spot
    owner_data = OWNER.objects.get(name=owner,address=address)
    owner_data.no_of_slots = owner_data.no_of_slots + 1
    owner_data.save()
    BOOK.objects.get(key_num=id).delete()
    return redirect('/main')

    

