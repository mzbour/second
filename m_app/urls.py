from django.urls import path
from . import views

urlpatterns = [
		path('', views.index),
        path('register',views.register),
        path('login',views.login),
        path('page1',views.page1),
        path('logout',views.logout),
        path('new/tree',views.new),
        path('show/<int:tid>',views.show),
        path('new/tree',views.add),
        path('addtree',views.addtree),
        path('user/account/',views.mange),
        path('delete/<int:tid>',views.delete),
        path('edit/<int:tid>',views.edit),
        path('update/<int:tid>',views.update),
        path('vv',views.vv),

        
        ]