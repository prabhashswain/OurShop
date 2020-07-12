from django.urls import path
from . import views
from .middleware.auth import auth_middleware

urlpatterns = [
    path('', views.index.as_view(),name='home'),
    path('signup', views.signup,name='signup'),
    path('login',views.Login.as_view(),name='login'),
    path('logout', views.logout,name='logout'),
    path('cart',auth_middleware(views.Cart.as_view()),name='cart'),
    path('checkout', views.Checkout.as_view(),name='checkout'),
    path('order',views.OrderView.as_view() ,name='order'),
]