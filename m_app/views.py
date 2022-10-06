from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
from urllib import request
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
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],visitors="1",email=request.POST['email'], password=pw_hash.decode())
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
    context={
"trees":Tree.objects.all()
    }

    return render(request,'page1.html',context)



def new(request):
    return render(request,'addtree.html')
def show(request,tid):
    uid=request.session['user_id']
    u=User.objects.get(id=uid)
    context={
        "mytree":Tree.objects.get(id=tid),
        "myallvisitors":Tree.objects.get(id=tid).users.all()
    }
    return render(request,'show.html',context)
def add(request):
    return render(request,'addtree.html')
def addtree(request):
    uid=request.session['user_id']
    p=User.objects.get(id=uid)
    t1=Tree.objects.create(Species=request.POST['speciliest'],location=request.POST['location'],region=request.POST['region'],dateplann=request.POST['dateplann'],planted_by=p)
    print("this tree is craeted sucressfully")
    vist=User.objects.get(id=uid)
    t1.users.add(vist)
    return redirect('/new/tree')

def mange(request):
    myid=request.session['user_id']
    my=User.objects.get(id=myid)
    context={
        "mytrees": my.user_trees.all()
        # "mytrees":Tree.user_trees.all(),
        # "mytrees":Tree.objects.all()
     }
    return render(request,'manage.html',context)


def edit(request,tid):
    tr=Tree.objects.get(id=tid)
    context={
        "mytree":tr
    }
    return render(request,'edit.html',context)
def delete(request,tid):
    t=Tree.objects.get(id=tid)
    t.delete()
    return redirect('/user/account')
def logout(request):
    del request.session['user_id'] 
    messages.error(request, "You have successfully logged out")
    return redirect('/')
def update(request,tid):
    t=Tree.objects.get(id=tid)
    t.Species=request.POST['speciliest']
    t.location=request.POST['location']
    t.region=request.POST['region']
    t.dateplann=request.POST['dateplann']
    t.save()
    return redirect('/page1')
def vv(request):
    myid=request.session['user_id']
    my=User.objects.get(id=myid)
    Tree.users.add(my)
    return redirect('/page1')
