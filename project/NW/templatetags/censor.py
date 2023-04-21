from django import template
from datetime import datetime
register = template.Library()



@register.filter()
def censor(message: str):
    stop_list = ['редиска', 'дурак', 'простофиля', 'мат', 'абракадабра', 'козел', 'баран', 'олух', 'забияка']  # непристойные выражения
    ln = len(stop_list)
    filtred_message = ''
    string = ''
    pattern = '*'  # чем заменять непристойные выражения
    for i in message:
        string += i
        string2 = string.lower()

        flag = 0
        for j in stop_list:
            if not string2 in j:
                flag += 1
            if string2 == j:
                filtred_message += pattern * len(string)
                flag -= 1
                string = ''

        if flag == ln:
            filtred_message += string
            string = ''

    if string2 != '' and string2 not in stop_list:
        filtred_message += string
    elif string2 != '':
        filtred_message += pattern * len(string)

    return filtred_message


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()

@register.simple_tag()
def current_time(format_string='%b %d %Y'):
   return datetime.utcnow().strftime(format_string)