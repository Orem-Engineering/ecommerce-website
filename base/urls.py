from django.urls import path
from base import views
# paths for base app
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logouts,name='logouts'),
    path('about/',views.aboutus,name='aboutus'),
    path('contactus/',views.contactus,name='contactus'),
    path('tracker/',views.tracker,name='tracker'),
    path('products/<int:myid>',views.productView,name='productView'),
    path('checkout/',views.purchase,name='checkout'),
    path('handlerequest/',views.handlerequest,name='handlerequest'),
]
