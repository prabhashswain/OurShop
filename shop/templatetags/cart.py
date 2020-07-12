from ..models.customer import Customer
from django import template
register=template.Library()

@register.filter(name="is_in_cart")
def is_in_cart(product,cart):
    keys=cart.keys()
    for key in keys:
        if int(key)==product.id:
            return True
    return False

@register.filter(name="cart_quantity")
def cart_quantity(product,cart):
    keys=cart.keys()
    for key in keys:
        if int(key)==product.id:
            return cart.get(key)
    return 0

@register.filter(name="price_total")
def price_total(product,cart):
    return product.price*cart_quantity(product,cart)

@register.filter(name="total_cart_price")
def total_cart_price(product,cart):
    sum=0
    for p in product:
        sum+=price_total(p,cart)
    return sum    

@register.filter(name="multiply")
def multiply(quantity,price):
    return quantity*price

@register.filter('userProfile')
def userProfile(user_id):
    return Customer.objects.get(user_id).first_name
