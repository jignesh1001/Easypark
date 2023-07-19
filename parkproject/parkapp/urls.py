from django.urls import path
from parkapp import views
urlpatterns = [
    path('',views.index),
    path('login',views.login),
    path('signup',views.signup),
    path('main',views.main),

  path('about',views.about),
  path('contactUs',views.contactUs),

    path('logout',views.userlogout),
    path('usertype',views.usertype),
    path('addinfo',views.addinfo),
    path('create_profile',views.crepro),
    path('profile',views.check_profile),
    path('delete_spot/<int:id>',views.delete_spot),
    path('book_spot/<int:id>',views.book_spot),
    path('accept/<int:id>',views.accept),
    path('decline/<int:id>',views.decline),
    path('free_slot/<int:id>',views.free_slot)
    

    # path('about',views.about), ##changing
    # path('search',views.search)
]
