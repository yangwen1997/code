from django import template
from my_blog.models import Entry,Category,Tag
register = template.Library()

@register.simple_tag
def get_recent_entries(num=5):
    return Entry.objects.all().order_by('created_time')[:num]
@register.simple_tag
def get_popular_entries(num=5):
    return Entry.objects.all().order_by('-visiting')[:num]
@register.simple_tag
def archives():
    return Entry.objects.dates('created_time','month',order='DESC')
@register.simple_tag
def get_entry_cont_of(year,month):
    return Entry.objects.filter(created_time__year=year,created__time_month=month).count()

@register.simple_tag
def get_tags():
    return Tag.objects.all()