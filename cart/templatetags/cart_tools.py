from django import template
from decimal import Decimal # More accurate result


register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * Decimal(quantity)