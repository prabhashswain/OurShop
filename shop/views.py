from django.shortcuts import render,redirect,HttpResponseRedirect
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.order import Order
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.hashers import make_password,check_password
from django.utils.decorators import method_decorator
from .middleware.auth import auth_middleware

class index(View):
    def get(self,request):
        product=None
        category=Category.objects.all()
        data={}
        category_id=request.GET.get("category")
        if category_id:
            product=Product.get_product_by_categoryid(category_id)
        else:
            product=Product.get_all_products()
        data['product']=product
        data['category']=category
        return render(request,"Eshop/index.html",data)
    def post(self,request):
        product=request.POST.get('product')  
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                else:
                    cart[product]=quantity+1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        request.session['cart']=cart
        return redirect('home')

def signup(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        password=request.POST.get('password')
        value={
            'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'contact':contact,
        }
        if not first_name:
            messages.error(request,"First name required")
            return render(request,"Eshop/signup.html",value)
        if len(first_name)<4:
            messages.error(request,"First name should greater than 4")
            return render(request,"Eshop/signup.html",value)
        if not last_name:
            messages.error(request,"Last name required")
            return render(request,"Eshop/signup.html",value)
        if len(last_name)<4:
            messages.error(request,"Last name should greater than 4")
            return render(request,"Eshop/signup.html",value)
        if not contact:
            messages.error(request,"phone number required")
            return render(request,"Eshop/signup.html",value)
        if len(contact)<10:
            messages.error(request,"phone number should greater than 10")
            return render(request,"Eshop/signup.html",value)
        if not password:
            messages.error(request,"password required")
            return render(request,"Eshop/signup.html",value)

        if Customer.objects.filter(email=email).exists():
            messages.error(request,"Email Already Exist")
            return render(request,"Eshop/signup.html",value) 
        else:
            customer=Customer(first_name=first_name,last_name=last_name,email=email,contact=contact,password=make_password(password))
            customer.register() 
        return redirect('login')
    else:
        return render(request,"Eshop/signup.html")

class Login(View):
    def get(self,request):
        return_url=None
        Login.return_url=request.GET.get('return_url')
        if request.session.get('customer'):
            return redirect('home')
        else:
            return render(request,"Eshop/login.html")
    def post(self,request):
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=Customer.objects.get(email=email)
        if customer:
            flag=check_password(password,customer.password)
            if flag:
                request.session['customer']=customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    return redirect('home')
            else:
                messages.error(request,"Invalid Credentials")
                return render(request,"Eshop/login.html",{'email':email})  
        else:
            messages.error(request,"Invalid Email Id")
            return render(request,"Eshop/login.html",{'email':email})  


def logout(request):
    try:
        print(request.session.get('customer'))
        del request.session['customer']
    except KeyError:  
        pass
    return redirect('login')

class Cart(View):
    def get(self,request):
        cart=request.session.get('cart')
        ids=list(cart.keys())
        product=Product.get_product_by_ids(ids)
        return render(request,"Eshop/cart.html",{'products':product})

class Checkout(View):
    def post(self,request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        customer=request.session.get('customer')
        cart=request.session.get('cart')
        products=Product.get_product_by_ids(list(cart.keys()))
        for product in products:
            order=Order(product=product,customer=Customer(id=customer),quantity=cart.get(str(product.id)),price=product.price,address=address,phone=phone)
            order.save()  
        request.session['cart']={}
        return redirect('cart')

class OrderView(View):
    @method_decorator(auth_middleware)
    def get(self,request):
        customer=request.session.get('customer')
        order=Order.get_product_by_customer(customer)
        return render(request,"Eshop/order.html",{'orders':order})