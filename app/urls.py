from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('product-detail/<int:id>/', views.product_detail, name='product-detail'),
    path('addtocart/', views.add_to_cart, name='add-to-cart'),
    path('showcart/', views.show_cart, name='show_cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('filter/<str:category>', views.filter, name='filter'),
    path('login/', views.user_login, name='login'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('logout/', views.user_logout, name='logout'),
    path('pluscart/', views.pluscart, name='pluscart'),
    path('minuscart/', views.minuscart, name='minuscart'),
    path('removecart/', views.removecart, name='removecart'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    path('search/', views.search, name='search'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
