from django import template
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
from .. import models
 
register = template.Library()
 
@register.filter
def user_url(username):
    return reverse('profile_detail', args=[username])
 
@register.filter
def user(username, postfix=''):
    url = user_url(username)
    user_obj = models.User.objects.get(username=username)
    return mark_safe('<a href="{0}{1}">{2}</a>'.format(url, postfix, f'{user_obj.get_full_name()} ({username})'))

@register.filter
def users(usernames, postfix=''):
    users_string = ""
    for username in usernames:
        users_string += user(username, postfix) + ", "
    return mark_safe(users_string[:-2])

@register.filter
def course_url(course):
    course_obj = models.Course.objects.get(pk=course)
    return course_obj.get_absolute_url()
 
@register.filter
def course(course, postfix=''):
    url = course_url(course)
    course_obj = models.Course.objects.get(pk=course)
    return mark_safe('<a href="{0}{1}">{2}</a>'.format(url, postfix, str(course_obj)))

@register.filter
def term_url(term):
    term_obj = models.Term.objects.get(pk=term)
    return term_obj.get_absolute_url()
 
@register.filter
def term(term, postfix=''):
    url = term_url(term)
    term_obj = models.Term.objects.get(pk=term)
    return mark_safe('<a href="{0}{1}">{2}</a>'.format(url, postfix, str(term_obj)))

@register.filter
def timetable_url(timetable):
    return reverse('view_timetable', args=[timetable])
 
@register.filter
def timetable(timetable, postfix=''):
    url = timetable_url(timetable)
    timetable_obj = models.Timetable.objects.get(pk=timetable)
    return mark_safe('<a href="{0}{1}">{2}</a>'.format(url, postfix, str(timetable_obj)))
