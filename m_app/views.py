from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    print("in the index method")
    if 'user' in request.session:    
        del request.session['user']
    return render (request, 'login.html')

def register(request):
    print("in the register method")
    if request.method =='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/')
        else:
            password=request.POST['password']
            pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash.decode())
            request.session['user']=request.POST['first_name']
            request.session['user_id']=new_user.id
            return redirect ('/')
    return redirect ('/')
def login(request):
    print('*'*80)
    print("in the login method")
    if request.method =='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user=User.objects.filter(email=request.POST['email'])
            logged_user=user[0]
            request.session['user'] = logged_user.first_name
            request.session['user_id']=logged_user.id
            return redirect ('/page1')
    else:
        return redirect ('/')

def page1(request):
    return render(request,'page1.html')
