from django import template

register = template.Library()

@register.filter
def cloudinary_resize(url, size='w_400,h_400,c_fill,f_auto,q_auto'):
    if 'res.cloudinary.com' in url:
        return url.replace('/upload/', f'/upload/{size}/')
    return url