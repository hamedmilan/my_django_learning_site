from django import template

register = template.Library()

@register.inclusion_tag('accounts/pass_change_message.html')
def pass_change_message(messages, login_link_flag):
    return {'messages': messages, 'login_link_flag': login_link_flag}

